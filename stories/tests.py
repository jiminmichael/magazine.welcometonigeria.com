from datetime import date
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from stories.models import State, Story, StoryImage, SavedStory


class StoriesApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='kayode_travels',
            email='kayode@example.com',
            password='kayodePassword123!',
            first_name='Kayode',
            last_name='Johnson',
        )

        self.state_osun = State.objects.create(name='Osun', slug='osun', code='OS')
        self.state_lagos = State.objects.create(name='Lagos', slug='lagos', code='LA')

        self.story1 = Story.objects.create(
            title='Art and Rivers in Osogbo',
            author=self.user,
            author_name='Kayode Johnson',
            author_email='kayode@example.com',
            state=self.state_osun,
            location='Osogbo',
            travel_date=date(2026, 7, 10),
            published_date=date(2026, 8, 1),
            preview='Exploring the groves and riverbanks.',
            experience='A wonderful travel journey exploring the sacred groves, quiet rivers, and artistic heritage of Osun state.',
            featured=True,
            popularity=100,
            status='published',
        )

        self.story2 = Story.objects.create(
            title='Lagos Lagoon Sunsets',
            author=self.user,
            author_name='Kayode Johnson',
            author_email='kayode@example.com',
            state=self.state_lagos,
            location='Victoria Island',
            travel_date=date(2026, 8, 15),
            published_date=date(2026, 8, 20),
            preview='Ferry rides along the lagoon.',
            experience='Crossing from Marina to the island on a clear late afternoon reveals the vibrant life of Lagos.',
            featured=False,
            popularity=50,
            status='published',
        )

    def test_state_list_api(self):
        response = self.client.get('/api/states/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        osun_item = next(item for item in response.data if item['name'] == 'Osun')
        self.assertEqual(osun_item['count'], 1)

    def test_stories_list_and_filters(self):
        # All published
        response = self.client.get('/api/stories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        # Filter by state
        osun_resp = self.client.get('/api/stories/?state=Osun')
        self.assertEqual(len(osun_resp.data), 1)
        self.assertEqual(osun_resp.data[0]['title'], 'Art and Rivers in Osogbo')

        # Filter by search
        search_resp = self.client.get('/api/stories/?q=lagoon')
        self.assertEqual(len(search_resp.data), 1)
        self.assertEqual(search_resp.data[0]['title'], 'Lagos Lagoon Sunsets')

        # Filter by featured
        featured_resp = self.client.get('/api/stories/?featured=true')
        self.assertEqual(len(featured_resp.data), 1)
        self.assertEqual(featured_resp.data[0]['title'], 'Art and Rivers in Osogbo')

    def test_story_detail_and_popularity_increment(self):
        initial_pop = self.story1.popularity
        response = self.client.get(f'/api/stories/{self.story1.slug}/')
        self.assertEqual(response.status_code, 200)
        self.story1.refresh_from_db()
        self.assertEqual(self.story1.popularity, initial_pop + 1)
        self.assertIn('related', response.data)

    def test_story_submission_with_image(self):
        image_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        test_photo = SimpleUploadedFile('trip.gif', image_content, content_type='image/gif')

        response = self.client.post('/api/stories/submit/', {
            'name': 'Bisi Akande',
            'email': 'bisi@example.com',
            'state': 'Osun',
            'location': 'Erin Ijesha',
            'travel_date': '2026-09-10',
            'title': 'The Seven Tiers of Erin Ijesha Waterfalls',
            'experience': 'Climbing each level of the Olumirin waterfalls in Erin Ijesha is a refreshing challenge with cold mountain waters.',
            'recommend': 'Absolutely',
            'travel_tips': 'Wear sturdy grip shoes and keep camera waterproof.',
            'photos': [test_photo],
        })
        self.assertEqual(response.status_code, 201)
        new_story = Story.objects.get(title='The Seven Tiers of Erin Ijesha Waterfalls')
        self.assertEqual(new_story.status, 'pending')
        self.assertEqual(new_story.images.count(), 1)

    def test_save_story_toggle(self):
        self.client.force_login(self.user)
        # Save
        save_resp = self.client.post(f'/api/stories/{self.story1.slug}/save/')
        self.assertEqual(save_resp.status_code, 200)
        self.assertTrue(save_resp.data['saved'])
        self.assertTrue(SavedStory.objects.filter(user=self.user, story=self.story1).exists())

        # Unsave
        unsave_resp = self.client.post(f'/api/stories/{self.story1.slug}/save/')
        self.assertEqual(unsave_resp.status_code, 200)
        self.assertFalse(unsave_resp.data['saved'])
        self.assertFalse(SavedStory.objects.filter(user=self.user, story=self.story1).exists())

    def test_user_stories_endpoint(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/stories/user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['submitted']), 2)
        self.assertEqual(response.data['stats']['published_count'], 2)
