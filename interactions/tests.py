from django.test import TestCase, Client
from interactions.models import NewsletterSubscription, ContactMessage


class InteractionsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_newsletter_subscription(self):
        # Valid subscription
        response = self.client.post('/api/interactions/newsletter/', {
            'email': 'subscriber@example.com',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewsletterSubscription.objects.filter(email='subscriber@example.com').exists())

        # Duplicate subscription should succeed gracefully
        dup_resp = self.client.post('/api/interactions/newsletter/', {
            'email': 'subscriber@example.com',
        }, content_type='application/json')
        self.assertEqual(dup_resp.status_code, 200)

        # Invalid email
        inv_resp = self.client.post('/api/interactions/newsletter/', {
            'email': 'invalid-email',
        }, content_type='application/json')
        self.assertEqual(inv_resp.status_code, 400)

    def test_contact_submission(self):
        response = self.client.post('/api/interactions/contact/', {
            'name': 'Fadekemi Oladele',
            'email': 'fadekemi@example.com',
            'subject': 'Question about visiting Yankari Game Reserve',
            'message': 'Hello, I loved the Kano story! Are there recent travel notes on Bauchi state and Yankari?',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ContactMessage.objects.filter(email='fadekemi@example.com').exists())
        msg = ContactMessage.objects.get(email='fadekemi@example.com')
        self.assertEqual(msg.name, 'Fadekemi Oladele')
