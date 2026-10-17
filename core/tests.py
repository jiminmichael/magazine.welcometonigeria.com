from django.test import TestCase, Client


class CorePagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages_render_and_csrf_cookie(self):
        pages = [
            '/',
            '/index.html',
            '/about.html',
            '/stories.html',
            '/story.html',
            '/states.html',
            '/state.html',
            '/share-story.html',
            '/travel-tips.html',
            '/contact.html',
            '/signin.html',
            '/signup.html',
            '/forgot-password.html',
            '/account.html',
            '/profile.html',
            '/privacy-policy.html',
            '/terms.html',
        ]

        for page in pages:
            response = self.client.get(page)
            self.assertEqual(
                response.status_code, 200,
                f"Page {page} failed with status {response.status_code}"
            )
            # Ensure CSRF cookie is delivered
            self.assertIn('csrftoken', response.cookies, f"CSRF cookie missing for {page}")

    def test_static_css_and_js_served(self):
        css_resp = self.client.get('/css/style.css')
        self.assertEqual(css_resp.status_code, 200)

        js_resp = self.client.get('/js/main.js')
        self.assertEqual(js_resp.status_code, 200)
