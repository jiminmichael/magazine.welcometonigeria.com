from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accounts.models import User
from stories.models import State, Story, StoryImage

NIGERIA_STATES = [
    ("Abia", "AB"),
    ("Adamawa", "AD"),
    ("Akwa Ibom", "AK"),
    ("Anambra", "AN"),
    ("Bauchi", "BA"),
    ("Bayelsa", "BY"),
    ("Benue", "BE"),
    ("Borno", "BO"),
    ("Cross River", "CR"),
    ("Delta", "DE"),
    ("Ebonyi", "EB"),
    ("Edo", "ED"),
    ("Ekiti", "EK"),
    ("Enugu", "EN"),
    ("Gombe", "GO"),
    ("Imo", "IM"),
    ("Jigawa", "JI"),
    ("Kaduna", "KD"),
    ("Kano", "KN"),
    ("Katsina", "KT"),
    ("Kebbi", "KE"),
    ("Kogi", "KO"),
    ("Kwara", "KW"),
    ("Lagos", "LA"),
    ("Nasarawa", "NA"),
    ("Niger", "NI"),
    ("Ogun", "OG"),
    ("Ondo", "ON"),
    ("Osun", "OS"),
    ("Oyo", "OY"),
    ("Plateau", "PL"),
    ("Rivers", "RI"),
    ("Sokoto", "SO"),
    ("Taraba", "TA"),
    ("Yobe", "YO"),
    ("Zamfara", "ZA"),
    ("FCT Abuja", "FC"),
]

def photo(photo_id, w=1000):
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&q=82"

SAMPLE_STORIES = [
    {
        "id": "sample-oshogbo",
        "title": "Following the river into Osogbo",
        "state": "Osun",
        "location": "Osogbo",
        "author": "Adaeze Okafor",
        "authorId": "adaeze-okafor",
        "authorEmail": "adaeze.okafor@example.com",
        "authorPhoto": photo("photo-1534528741775-53994a69daeb", 160),
        "date": "2026-08-12",
        "publishedDate": "2026-09-02",
        "preview": "A slow morning beside the river became a lesson in the living art, stories and generosity of Osogbo.",
        "story": (
            "I arrived in Osogbo with a loose plan and enough time to change it. The city met me in layers: "
            "the hum of the morning market, the shade of old trees and the sound of conversation that seemed "
            "to carry from one street to the next.\n\n"
            "The walk beside the river was the part I had imagined, but the people I met made the day. A local "
            "guide shared the history behind the works along the route, and suddenly every turn felt less like "
            "a view and more like an invitation to listen.\n\n"
            "I left with a camera full of details and a notebook full of names. Give yourself room to wander, "
            "ask thoughtful questions and let the day take its own shape."
        ),
        "images": [
            photo("photo-1516026672322-bc52d61a55d5"),
            photo("photo-1500530855697-b586d89ba3ee"),
            photo("photo-1470770841072-f978cf4d019e"),
        ],
        "tips": "Start early for cooler walking. Ask before photographing people, and leave time to hear the stories behind the places.",
        "recommendation": "Absolutely. Go with curiosity and make time for a local guide.",
        "featured": True,
        "popularity": 184,
    },
    {
        "id": "sample-lagos",
        "title": "Lagos, best discovered between the plans",
        "state": "Lagos",
        "location": "Lagos Island",
        "author": "Tunde Akinyemi",
        "authorId": "tunde-akinyemi",
        "authorEmail": "tunde.akinyemi@example.com",
        "authorPhoto": photo("photo-1500648767791-00dcc994a43e", 160),
        "date": "2026-07-18",
        "publishedDate": "2026-08-21",
        "preview": "I stopped trying to fit Lagos into a checklist and started following the conversations, the ferries and the afternoon light.",
        "story": (
            "Lagos moves at a pace that asks you to pay attention. I spent my first day rushing between places "
            "and my second day doing almost nothing on schedule. The second day is the one I still talk about.\n\n"
            "We crossed the lagoon, found lunch through a recommendation from a stranger and let the afternoon "
            "stretch out. From the water, the city looked both familiar and entirely new. Back on the island, "
            "small details kept pulling me in: a doorway painted bright blue, a musician tuning up, a table "
            "of fruit arranged like a still life.\n\n"
            "My advice is to plan the essentials, then leave a little space. The best moments were the ones "
            "I had not tried to book."
        ),
        "images": [
            photo("photo-1518391846015-55a9cc003b25"),
            photo("photo-1517248135467-4c7edcad34c4"),
            photo("photo-1500534623283-312aade485b7"),
        ],
        "tips": "Give yourself extra time for local transport. Keep essentials close and ask residents for current, practical advice.",
        "recommendation": "Yes, especially for travellers who enjoy cities with many layers.",
        "featured": True,
        "popularity": 212,
    },
    {
        "id": "sample-cross-river",
        "title": "A quieter kind of adventure in Cross River",
        "state": "Cross River",
        "location": "Obudu",
        "author": "Sheriff Bello",
        "authorId": "sheriff-bello",
        "authorEmail": "sheriff.bello@example.com",
        "authorPhoto": photo("photo-1506794778202-cad84cf45f1d", 160),
        "date": "2026-06-04",
        "publishedDate": "2026-07-12",
        "preview": "The road north kept opening into green hills, cool air and the kind of quiet that makes you notice everything.",
        "story": (
            "The journey towards Obudu was as much a part of the trip as the days we spent there. The landscape "
            "changed gradually, and then all at once: greener slopes, a cooler breeze and a horizon that seemed "
            "to keep moving farther away.\n\n"
            "I travelled with family and we took the long stops seriously. We shared food, spoke with people along "
            "the way and watched the clouds settle over the hills. There is something grounding about a place that "
            "asks you to slow down without making a show of it.\n\n"
            "Bring layers for the cooler evenings and check local travel conditions before you leave. Most of all, "
            "leave enough time to enjoy the road."
        ),
        "images": [
            photo("photo-1464822759023-fed622ff2c3b"),
            photo("photo-1472396961693-142e6e269027"),
            photo("photo-1441974231531-c6227db76b6e"),
        ],
        "tips": "Pack a light jacket and confirm road and weather conditions before travel. Start longer drives early in the day.",
        "recommendation": "Yes. It is a lovely change of pace for anyone who enjoys open landscapes.",
        "featured": True,
        "popularity": 138,
    },
    {
        "id": "sample-abuja",
        "title": "The small trails that changed my Abuja weekend",
        "state": "FCT Abuja",
        "location": "Abuja",
        "author": "Mariam Yusuf",
        "authorId": "mariam-yusuf",
        "authorEmail": "mariam.yusuf@example.com",
        "authorPhoto": photo("photo-1531123897727-8f129e1688ce", 160),
        "date": "2026-05-09",
        "publishedDate": "2026-06-18",
        "preview": "A weekend close to home turned into a collection of early walks, long breakfasts and new ways to see the capital.",
        "story": (
            "I thought I knew Abuja because I knew the roads I used every week. Over one unhurried weekend, "
            "I found another version of the city by taking the morning slowly and saying yes to a few local "
            "recommendations.\n\n"
            "We started before the day warmed up, walked a familiar route at a different pace and stopped for "
            "breakfast somewhere we had driven past dozens of times. The conversations were easy; the views, "
            "even more so. I came away reminded that travel can begin with a different turn on a road you already know.\n\n"
            "Choose one part of the city rather than trying to cover everything. The best discoveries happened "
            "when we were not watching the clock."
        ),
        "images": [
            photo("photo-1500534314209-a25ddb2bd429"),
            photo("photo-1501785888041-af3ef285b470"),
            photo("photo-1470252649378-9c29740c9fa8"),
        ],
        "tips": "Go early to enjoy outdoor walks before the heat builds. Ask locally about access and conditions, then keep your plan flexible.",
        "recommendation": "Definitely. Abuja rewards a slower, more curious visit.",
        "featured": False,
        "popularity": 95,
    },
    {
        "id": "sample-kano",
        "title": "Kano mornings, told one conversation at a time",
        "state": "Kano",
        "location": "Kano",
        "author": "Ibrahim Sani",
        "authorId": "ibrahim-sani",
        "authorEmail": "ibrahim.sani@example.com",
        "authorPhoto": photo("photo-1507003211169-0a1dd7228f2d", 160),
        "date": "2026-04-22",
        "publishedDate": "2026-05-30",
        "preview": "The city woke up around me in colour and sound, and every conversation added a little more context.",
        "story": (
            "I began my visit with a list of places and finished it with a list of people to thank. Kano has a "
            "rhythm all of its own, and I found that a patient morning was the best way to meet it.\n\n"
            "At each stop I learned a little more by listening. A shopkeeper told me how long his family had "
            "worked in the neighbourhood; a driver pointed out a route I would never have found alone. By the "
            "end of the day, the city felt less like a destination and more like a series of generous introductions.\n\n"
            "Wear comfortable shoes, bring water and listen before you take photographs. It made all the difference to my visit."
        ),
        "images": [
            photo("photo-1494783367193-149034c05e8f"),
            photo("photo-1488646953014-85cb44e25828"),
            photo("photo-1500534623283-312aade485b7"),
        ],
        "tips": "Dress for the weather, carry water and ask permission before taking portraits. A local guide can add useful context.",
        "recommendation": "Yes. Take your time and let local voices lead.",
        "featured": False,
        "popularity": 76,
    },
]


class Command(BaseCommand):
    help = "Seed Nigeria states, initial sample travellers, and sample travel stories."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Nigerian states...")
        state_map = {}
        for index, (state_name, code) in enumerate(NIGERIA_STATES, start=1):
            state_obj, created = State.objects.update_or_create(
                name=state_name,
                defaults={
                    "slug": slugify(state_name),
                    "code": code,
                    "order": index,
                }
            )
            state_map[state_name] = state_obj
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(state_map)} states."))

        self.stdout.write("Seeding sample stories and authors...")
        for story_data in SAMPLE_STORIES:
            author_id = story_data["authorId"]
            name_parts = story_data["author"].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            user, _ = User.objects.get_or_create(
                username=author_id,
                defaults={
                    "email": story_data["authorEmail"],
                    "first_name": first_name,
                    "last_name": last_name,
                    "avatar_url": story_data["authorPhoto"],
                    "bio": f"Travel contributor from Nigeria exploring {story_data['state']} and beyond.",
                }
            )
            if not user.has_usable_password():
                user.set_password("wtnPassword2026!")
                user.save()

            state = state_map.get(story_data["state"])
            travel_date = datetime.strptime(story_data["date"], "%Y-%m-%d").date()
            pub_date = datetime.strptime(story_data["publishedDate"], "%Y-%m-%d").date() if story_data.get("publishedDate") else None

            story, created = Story.objects.update_or_create(
                legacy_id=story_data["id"],
                defaults={
                    "title": story_data["title"],
                    "slug": slugify(story_data["title"]),
                    "author": user,
                    "author_name": story_data["author"],
                    "author_email": story_data["authorEmail"],
                    "author_photo_url": story_data["authorPhoto"],
                    "state": state,
                    "location": story_data["location"],
                    "travel_date": travel_date,
                    "published_date": pub_date,
                    "preview": story_data["preview"],
                    "experience": story_data["story"],
                    "tips": story_data["tips"],
                    "recommendation": story_data["recommendation"],
                    "featured": story_data["featured"],
                    "popularity": story_data["popularity"],
                    "status": "published",
                }
            )

            # Add images
            story.images.all().delete()
            for idx, img_url in enumerate(story_data["images"], start=1):
                StoryImage.objects.create(
                    story=story,
                    image_url=img_url,
                    order=idx,
                )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(SAMPLE_STORIES)} travel stories and authors."))

