from django.core import mail
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

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


class ContentApiTests(APITestCase):
    def test_root_lists_endpoints(self):
        data = self.client.get(reverse('api:root')).json()
        self.assertEqual(set(data), {'site', 'home', 'about', 'enquiries'})

    def test_site(self):
        data = self.client.get(reverse('api:site')).json()
        self.assertEqual(data['site_name'], 'Ban2Plans')
        self.assertEqual(data['whatsapp_number'], '919412833444')
        self.assertEqual(data['profile']['name'], 'Shashi Darshan')
        self.assertTrue(data['profile']['image'].startswith('http://testserver/static/'))

    def test_home_has_sections_and_absolute_image_urls(self):
        data = self.client.get(reverse('api:home')).json()
        for key in ('hero', 'stats', 'intro', 'services', 'sessions', 'why_me',
                    'process', 'client_types', 'testimonials', 'faqs'):
            self.assertIn(key, data)
        self.assertTrue(data['hero']['image'].endswith('/static/homepage/img/banquet-hall.jpg'))
        self.assertTrue(all(s['image'].startswith('http://') for s in data['services']))

    def test_about(self):
        data = self.client.get(reverse('api:about')).json()
        self.assertEqual(data['experience'][0]['role'], 'Assistant Sales Manager')
        self.assertEqual(len(data['education']), 4)

    def test_content_is_read_only(self):
        self.assertEqual(self.client.post(reverse('api:home'), {}).status_code, 405)

    def test_cors_allows_frontend_dev_server(self):
        resp = self.client.get(reverse('api:site'), HTTP_ORIGIN='http://127.0.0.1:5500')
        self.assertEqual(resp['Access-Control-Allow-Origin'], 'http://127.0.0.1:5500')


@override_settings(ENQUIRY_EMAIL_TO='inbox@example.com')
class EnquiryApiTests(APITestCase):
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
        self.assertEqual(mail.outbox[0].subject,
                         'New enquiry: Corporate Events & Conferences – Priya Sharma')

    def test_missing_email_is_rejected(self):
        resp = self.client.post(self.url, dict(VALID, email=''), format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('email', resp.json()['errors'])
        self.assertEqual(len(mail.outbox), 0)

    def test_unknown_event_type_is_rejected(self):
        resp = self.client.post(self.url, dict(VALID, event_type='Space launch'), format='json')
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
        self.assertIn('Retry-After', resp)
        self.assertEqual(len(mail.outbox), 30)

    def test_get_lists_event_types(self):
        data = self.client.get(self.url).json()
        self.assertIn('Other', data['event_types'])
