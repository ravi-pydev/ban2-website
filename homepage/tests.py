import tempfile
from email.utils import parseaddr
from pathlib import Path
from unittest import mock

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from . import models
from .seed import SEED_FILE, load_sql_file

VALID = {
    'name': 'Priya Sharma',
    'email': 'priya@example.com',
    'phone': '+91 9800000010',
    'company': 'Acme Technologies',
    'event_type': 'Corporate Events & Conferences',
    'guests': '120',
    'date': '2026-12-15',
    'event_location': 'Leela Ambience, Gurugram',
    'message': 'Annual sales meet with lunch and AV.',
}


class SeedDataTests(TestCase):
    def test_seed_fills_every_content_table(self):
        load_sql_file()
        counts = {
            models.SiteSettings: 1, models.Profile: 1, models.Service: 6, models.EventSession: 6,
            models.Testimonial: 3, models.Faq: 4, models.Stat: 4, models.SellingPoint: 4,
            models.ProcessStep: 5, models.ClientType: 6, models.Experience: 3,
            models.ExperiencePoint: 14, models.Education: 4, models.Highlight: 4,
            models.Skill: 6, models.Language: 2, models.Interest: 4, models.PageSection: 3,
        }
        for model, expected in counts.items():
            self.assertEqual(model.objects.count(), expected, model.__name__)

    def test_seed_can_be_rerun_and_keeps_enquiries(self):
        load_sql_file()
        models.Enquiry.objects.create(name='Kept', email='k@example.com', event_type='Other',
                                      service=models.Service.objects.first())
        load_sql_file()
        self.assertEqual(models.Service.objects.count(), 6)
        enquiry = models.Enquiry.objects.get()
        self.assertEqual(enquiry.name, 'Kept')
        self.assertIsNone(enquiry.service)


class FrontendViewTests(TestCase):
    def test_page_urls_serve_react_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'index.html').write_text('<div id="root"></div>', encoding='utf-8')
            with override_settings(FRONTEND_DIST=Path(tmp)):
                for url in ('/', '/about/', '/reviews/', '/some/unknown/page'):
                    resp = self.client.get(url)
                    self.assertEqual(resp.status_code, 200, url)
                    self.assertContains(resp, 'id="root"')

    def test_missing_build_explains_what_to_do(self):
        with tempfile.TemporaryDirectory() as tmp:
            with override_settings(FRONTEND_DIST=Path(tmp)):
                resp = self.client.get('/about/')
        self.assertEqual(resp.status_code, 503)
        self.assertContains(resp, 'npm run build', status_code=503)

    def test_api_urls_are_not_caught(self):
        self.assertEqual(self.client.get('/api/does-not-exist/').status_code, 404)


class DummyTestimonialsTests(TestCase):
    DUMMY_FILE = SEED_FILE.parent / '14_dummy_testimonials.sql'

    def test_dummy_file_replaces_samples_and_keeps_real_testimonials(self):
        load_sql_file()
        real = models.Testimonial.objects.create(
            client_name='Real Client', quote='Real feedback.', consent_given=True, is_published=True)
        load_sql_file(self.DUMMY_FILE)
        load_sql_file(self.DUMMY_FILE)  # re-running must not duplicate rows
        self.assertEqual(models.Testimonial.objects.filter(consent_given=False).count(), 6)
        self.assertTrue(models.Testimonial.objects.filter(pk=real.pk).exists())
        self.assertEqual(
            models.Testimonial.objects.filter(event_session__isnull=False).count(), 5)


class EmptyDatabaseTests(APITestCase):
    def test_site_reports_missing_content(self):
        resp = self.client.get(reverse('api:site'))
        self.assertEqual(resp.status_code, 503)
        self.assertIn('load_seed', resp.json()['detail'])

    def test_home_reports_missing_content(self):
        self.assertEqual(self.client.get(reverse('api:home')).status_code, 503)


class ContentApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_sql_file()

    def test_root_lists_endpoints(self):
        data = self.client.get(reverse('api:root')).json()
        self.assertEqual(set(data), {'site', 'home', 'about', 'enquiries', 'reviews', 'feedback'})

    def test_site(self):
        data = self.client.get(reverse('api:site')).json()
        self.assertEqual(data['site_name'], 'Event & Experience by Ban2')
        self.assertEqual(data['whatsapp_number'], '919050824511')
        profile = data['profile']
        self.assertEqual(profile['name'], 'Shashi Darshan')
        self.assertEqual(profile['dob'], '08 May 1999')
        self.assertEqual(profile['phone'], '')
        self.assertEqual(profile['service_area'], 'Delhi NCR & across India')
        self.assertTrue(profile['image'].startswith('http://testserver/static/'))

    def test_home_reads_tables(self):
        data = self.client.get(reverse('api:home')).json()
        self.assertEqual(len(data['services']), 6)
        self.assertEqual(data['services'][0]['title'], 'Corporate Events & Conferences')
        self.assertTrue(data['services'][0]['image'].endswith('/static/homepage/img/conference.jpg'))
        self.assertEqual(data['faqs'][0]['q'], 'What size of events do you handle?')
        self.assertEqual(data['process'][0]['title'], 'Consultation')
        self.assertEqual(data['client_types'][0], 'Multinational corporates')
        self.assertTrue(all(t['sample'] for t in data['testimonials']))
        self.assertEqual(data['testimonials'][0]['role'], 'Designation, Company')

    def test_home_page_sections_come_from_db(self):
        data = self.client.get(reverse('api:home')).json()
        hero, intro, cta = data['hero'], data['intro'], data['cta']
        self.assertEqual(hero['heading'], 'Events that run on time, on budget and on brand.')
        self.assertTrue(hero['text'].startswith('From boardroom meetings'))
        self.assertTrue(hero['image'].endswith('/static/homepage/img/banquet-hall.jpg'))
        self.assertEqual(hero['button'], 'Plan my event')
        self.assertEqual(intro['kicker'], 'Why hire a hospitality professional')
        self.assertEqual(len(intro['paragraphs']), 2)
        self.assertTrue(intro['paragraphs'][1].startswith('That experience means'))
        self.assertEqual(intro['items'], ['Venue, menu and AV in one plan', 'Transparent quotations',
                                          'One point of contact, start to finish',
                                          'On-site coordination on the day'])
        self.assertEqual(cta['heading'], 'Have an event coming up?')
        self.assertEqual(cta['button'], 'Get a free consultation')

    def test_inactive_section_is_hidden(self):
        models.PageSection.objects.filter(key='cta').update(is_active=False)
        self.assertIsNone(self.client.get(reverse('api:home')).json()['cta'])

    def test_hidden_rows_are_not_returned(self):
        models.Service.objects.filter(slug='social-celebrations').update(is_active=False)
        models.Testimonial.objects.filter(id=1).update(is_published=False)
        data = self.client.get(reverse('api:home')).json()
        self.assertEqual(len(data['services']), 5)
        self.assertEqual(len(data['testimonials']), 2)

    def test_consented_testimonial_is_not_sample(self):
        models.Testimonial.objects.filter(id=1).update(consent_given=True)
        data = self.client.get(reverse('api:home')).json()
        self.assertFalse(data['testimonials'][0]['sample'])

    def test_about(self):
        data = self.client.get(reverse('api:about')).json()
        current = data['experience'][0]
        self.assertEqual(current['role'], 'Assistant Sales Manager')
        self.assertEqual(current['period'], 'Apr 2026 – Present')
        self.assertEqual(len(current['points']), 6)
        self.assertEqual(data['experience'][2]['period'], 'Oct 2022 – Dec 2024')
        self.assertEqual(data['education'][0]['date'], 'Oct 2022')
        self.assertEqual(data['languages'][0], {'name': 'English',
                                                'level': 'Full professional proficiency',
                                                'percent': 85})
        self.assertEqual(data['skills'][0], 'Leadership')

    def test_content_is_read_only(self):
        self.assertEqual(self.client.post(reverse('api:home'), {}).status_code, 405)

    def test_cors_allows_frontend_dev_server(self):
        resp = self.client.get(reverse('api:site'), HTTP_ORIGIN='http://127.0.0.1:5500')
        self.assertEqual(resp['Access-Control-Allow-Origin'], 'http://127.0.0.1:5500')


FEEDBACK = {
    'name': 'Kavita Rao',
    'email': 'kavita@example.com',
    'company': 'Example Corp',
    'role': 'Admin Head',
    'rating': 4,
    'feedback': 'Smooth planning and great coordination with the hotel team.',
    'consent': True,
}


class ReviewsAndFeedbackTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_sql_file()
        models.SiteSettings.objects.update(enquiry_email='inbox@example.com')
        models.Testimonial.objects.all().delete()
        for name, rating, consent in [('Low', 3, True), ('Top', 5, True), ('Mid', 4, False)]:
            models.Testimonial.objects.create(client_name=name, quote=f'{name} review.',
                                              rating=rating, consent_given=consent,
                                              is_published=True)
        models.Testimonial.objects.create(client_name='Hidden', quote='Not published.', rating=5)

    def setUp(self):
        cache.clear()

    def test_reviews_sorted_high_to_low_with_summary(self):
        data = self.client.get(reverse('api:reviews')).json()
        self.assertEqual([r['name'] for r in data['reviews']], ['Top', 'Mid', 'Low'])
        self.assertEqual(data['summary']['count'], 3)
        self.assertEqual(data['summary']['average'], 4.0)
        self.assertEqual(data['summary']['breakdown'][0], {'stars': 5, 'count': 1})
        self.assertEqual(data['summary']['breakdown'][4], {'stars': 1, 'count': 0})
        self.assertTrue(data['reviews'][1]['sample'])  # no consent

    def test_home_includes_reviews(self):
        data = self.client.get(reverse('api:home')).json()
        self.assertEqual(data['reviews']['summary']['count'], 3)
        self.assertIn('id', data['sessions'][0])

    def test_feedback_is_saved_unpublished_and_owner_emailed(self):
        session = models.EventSession.objects.get(title='Gala dinners')
        resp = self.client.post(reverse('api:feedback'), dict(FEEDBACK, event_session=session.pk),
                                format='json')
        self.assertEqual(resp.status_code, 201)
        review = models.Testimonial.objects.get(pk=resp.json()['id'])
        self.assertFalse(review.is_published)
        self.assertTrue(review.consent_given)
        self.assertEqual(review.source, models.Testimonial.Source.WEBSITE)
        self.assertEqual(review.client_email, 'kavita@example.com')
        self.assertEqual(review.event_session, session)
        self.assertIsNotNone(review.received_on)
        # Not visible until approved
        names = [r['name'] for r in self.client.get(reverse('api:reviews')).json()['reviews']]
        self.assertNotIn('Kavita Rao', names)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ['inbox@example.com'])
        self.assertEqual(msg.reply_to, ['kavita@example.com'])
        self.assertIn('4★ feedback from Kavita Rao', msg.subject)
        self.assertIn('Event           : Gala dinners', msg.body)
        self.assertIn(f'/admin/homepage/testimonial/{review.pk}/change/', msg.body)

    def test_feedback_without_consent_is_flagged(self):
        resp = self.client.post(reverse('api:feedback'), dict(FEEDBACK, consent=False), format='json')
        self.assertFalse(models.Testimonial.objects.get(pk=resp.json()['id']).consent_given)
        self.assertIn('NO — do not publish', mail.outbox[0].body)

    def test_feedback_validation(self):
        for bad in ({'rating': 0}, {'rating': 6}, {'feedback': 'Too short'}, {'email': 'nope'}):
            resp = self.client.post(reverse('api:feedback'), dict(FEEDBACK, **bad), format='json')
            self.assertEqual(resp.status_code, 400, bad)
            self.assertIn(next(iter(bad)), resp.json()['errors'])

    def test_feedback_get_lists_published_events(self):
        models.EventSession.objects.filter(title='Team offsites').update(is_published=False)
        events = self.client.get(reverse('api:feedback')).json()['events']
        titles = [e['title'] for e in events]
        self.assertIn('Gala dinners', titles)
        self.assertNotIn('Team offsites', titles)
        self.assertEqual(set(events[0]), {'id', 'title'})

    def test_feedback_unknown_event_is_rejected(self):
        resp = self.client.post(reverse('api:feedback'), dict(FEEDBACK, event_session=99999),
                                format='json')
        self.assertEqual(resp.status_code, 400)

    def test_feedback_honeypot(self):
        before = models.Testimonial.objects.count()
        resp = self.client.post(reverse('api:feedback'), dict(FEEDBACK, website='spam'), format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(models.Testimonial.objects.count(), before)
        self.assertEqual(len(mail.outbox), 0)


class TestimonialAdminTests(TestCase):
    def test_publish_action_skips_reviews_without_consent(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser('admin', 'admin@example.com', 'pass12345')
        self.client.login(username='admin', password='pass12345')
        ok = models.Testimonial.objects.create(client_name='Yes', quote='q', consent_given=True)
        no = models.Testimonial.objects.create(client_name='No', quote='q', consent_given=False)
        self.client.post(reverse('admin:homepage_testimonial_changelist'),
                         {'action': 'publish', '_selected_action': [ok.pk, no.pk]})
        ok.refresh_from_db()
        no.refresh_from_db()
        self.assertTrue(ok.is_published)
        self.assertFalse(no.is_published)


class EnquiryApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_sql_file()
        models.SiteSettings.objects.update(enquiry_email='inbox@example.com')

    def setUp(self):
        cache.clear()
        self.url = reverse('api:enquiries')

    def test_valid_enquiry_sends_email(self):
        resp = self.client.post(self.url, VALID, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json()['ok'])
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.to, ['inbox@example.com'])
        self.assertEqual(msg.reply_to, ['priya@example.com'])
        self.assertEqual(
            msg.subject,
            'New enquiry: Corporate Events & Conferences – Priya Sharma, Acme Technologies',
        )
        self.assertIn('Preferred date  : 15 Dec 2026', msg.body)
        self.assertIn('Guests          : 120', msg.body)
        self.assertIn('Event location  : Leela Ambience, Gurugram', msg.body)
        self.assertIn('from the Event & Experience by Ban2 website', msg.body)
        self.assertEqual(parseaddr(msg.from_email)[0], 'Event & Experience by Ban2 Website')

    def test_enquiry_is_saved_to_database(self):
        resp = self.client.post(self.url, VALID, format='json', HTTP_USER_AGENT='TestBrowser/1.0')
        enquiry = models.Enquiry.objects.get(pk=resp.json()['id'])
        self.assertEqual(enquiry.name, 'Priya Sharma')
        self.assertEqual(enquiry.event_location, 'Leela Ambience, Gurugram')
        self.assertEqual(enquiry.guests, 120)
        self.assertEqual(str(enquiry.preferred_date), '2026-12-15')
        self.assertEqual(enquiry.service.title, 'Corporate Events & Conferences')
        self.assertEqual(enquiry.status, models.Enquiry.Status.NEW)
        self.assertEqual(enquiry.user_agent, 'TestBrowser/1.0')
        self.assertTrue(enquiry.email_sent)

    def test_failed_email_still_saves_enquiry(self):
        with mock.patch('homepage.views.EmailMessage.send', side_effect=OSError('SMTP down')):
            resp = self.client.post(self.url, VALID, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertFalse(resp.json()['email_sent'])
        self.assertFalse(models.Enquiry.objects.get().email_sent)

    def test_form_encoded_post_also_works(self):
        resp = self.client.post(self.url, VALID)
        self.assertEqual(resp.status_code, 201)

    def test_blank_optional_fields_show_dash(self):
        data = dict(VALID, company='', phone='', guests='', date='', event_location='', message='')
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        body = mail.outbox[0].body
        self.assertIn('Company         : –', body)
        self.assertIn('Guests          : –', body)
        self.assertIn('Preferred date  : –', body)
        self.assertIn('Event location  : –', body)
        self.assertEqual(models.Enquiry.objects.get().event_location, '')

    def test_event_location_is_optional(self):
        data = {k: v for k, v in VALID.items() if k != 'event_location'}
        self.assertEqual(self.client.post(self.url, data, format='json').status_code, 201)

    def test_event_location_too_long_is_rejected(self):
        resp = self.client.post(self.url, dict(VALID, event_location='x' * 151), format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('event_location', resp.json()['errors'])

    def test_missing_email_is_rejected(self):
        resp = self.client.post(self.url, dict(VALID, email=''), format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('email', resp.json()['errors'])
        self.assertEqual(len(mail.outbox), 0)

    def test_event_types_follow_services_table(self):
        self.assertIn('Other', self.client.get(self.url).json()['event_types'])
        models.Service.objects.filter(title='MICE Planning').update(is_active=False)
        resp = self.client.post(self.url, dict(VALID, event_type='MICE Planning'), format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('event_type', resp.json()['errors'])

    def test_honeypot_sends_nothing(self):
        resp = self.client.post(self.url, dict(VALID, website='http://spam.example'), format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Enquiry.objects.count(), 0)

    def test_rate_limit(self):
        for _ in range(30):
            self.client.post(self.url, VALID, format='json')
        resp = self.client.post(self.url, VALID, format='json')
        self.assertEqual(resp.status_code, 429)
        self.assertTrue(resp.json()['detail'].startswith('Too many enquiries.'))
        self.assertEqual(len(mail.outbox), 30)
