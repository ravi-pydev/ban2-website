import tempfile
from pathlib import Path

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from . import models
from .seed import load_sql_file

VALID = {
    'name': 'Priya Sharma',
    'email': 'priya@example.com',
    'phone': '+91 9800000010',
    'company': 'Acme Technologies',
    'event_type': 'Corporate Events & Conferences',
    'guests': '120',
    'date': '2026-12-15',
    'message': 'Annual sales meet in Gurugram.',
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
                for url in ('/', '/about/', '/some/unknown/page'):
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
        self.assertEqual(set(data), {'site', 'home', 'about', 'enquiries'})

    def test_site(self):
        data = self.client.get(reverse('api:site')).json()
        self.assertEqual(data['site_name'], 'Ban2Plans')
        self.assertEqual(data['whatsapp_number'], '919412833444')
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

    def test_form_encoded_post_also_works(self):
        resp = self.client.post(self.url, VALID)
        self.assertEqual(resp.status_code, 201)

    def test_blank_optional_fields_show_dash(self):
        data = dict(VALID, company='', phone='', guests='', date='', message='')
        resp = self.client.post(self.url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        body = mail.outbox[0].body
        self.assertIn('Company         : –', body)
        self.assertIn('Guests          : –', body)
        self.assertIn('Preferred date  : –', body)

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

    def test_rate_limit(self):
        for _ in range(30):
            self.client.post(self.url, VALID, format='json')
        resp = self.client.post(self.url, VALID, format='json')
        self.assertEqual(resp.status_code, 429)
        self.assertTrue(resp.json()['detail'].startswith('Too many enquiries.'))
        self.assertEqual(len(mail.outbox), 30)
