# Welcome to Nigeria Travel Magazine - Full Stack Platform

A community travel magazine web platform dedicated to real travel stories, photographic journeys, and notes from across Nigeria's 36 states and the Federal Capital Territory (Abuja).

This platform combines a lightweight, bespoke responsive frontend with a secure, production-ready Django backend with PostgreSQL/SQLite database persistence, Django Admin editorial review workflows, file storage, and session authentication.

---

## 1. System Architecture

```
magazine.welcometonigeria.com/
├── wtn_project/                 # Main Django project package
│   ├── settings.py              # Environment-driven settings (decouple, dj-database-url, WhiteNoise)
│   ├── urls.py                  # API, Admin, Static & Media, Core page routers
│   ├── wsgi.py / asgi.py        # WSGI / ASGI entrypoints
├── accounts/                    # Contributor authentication, profile, and session management
│   ├── models.py                # Custom User model (avatar, bio, email login)
│   ├── serializers.py           # DRF serializers for auth and profile updates
│   ├── views.py                 # Signup, signin, signout, current user, profile
│   └── urls.py                  # /api/auth/* endpoints
├── stories/                     # State directory, travel narratives, images, and saved stories
│   ├── models.py                # State, Story, StoryImage, SavedStory
│   ├── serializers.py           # Story, State, Submission serializers
│   ├── views.py                 # Story list, detail, submissions, states, saves
│   ├── admin.py                 # Admin dashboard with 'Approve & Publish' and 'Feature' actions
│   ├── management/commands/     # 'seed_initial_data' and 'create_admin'
│   └── urls.py                  # /api/stories/* and /api/states/
├── interactions/                # Community newsletter and direct contact submissions
│   ├── models.py                # NewsletterSubscription and ContactMessage
│   ├── views.py                 # Newsletter & contact API handlers with email dispatch
│   └── urls.py                  # /api/interactions/*
├── core/                        # Direct template views, CSRF cookie delivery, static routes
│   └── views.py                 # render_page view with @ensure_csrf_cookie
├── css/ & js/                   # Responsive styles and client-side modules
├── media/                       # User-uploaded story photographs and profile avatars
├── staticfiles/                 # Collected static assets for WhiteNoise
├── requirements.txt             # Production & development dependencies
└── .env.example                 # Environment variable templates
```

---

## 2. Requirements & Dependencies

- Python 3.10+
- Django 4.2+ (LTS)
- Django REST Framework 3.14+
- Pillow (Image uploads & processing)
- WhiteNoise (Production static file serving)
- Python Decouple (Environment variable configuration)
- dj-database-url (Database connection string parsing)
- Gunicorn (Production WSGI server)
- Psycopg2-binary (PostgreSQL production database adapter)

---

## 3. Quickstart & Local Setup

### Step 1: Clone and create a virtual environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux / macOS:
source venv/bin/activate
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Linux / macOS
```

### Step 4: Run Database Migrations
```bash
python manage.py migrate
```

### Step 5: Seed Nigerian States and Initial Sample Stories
Populate all 36 Nigerian states + FCT Abuja, sample authors, and published stories:
```bash
python manage.py seed_initial_data
```

### Step 6: Create an Administrator Account
Run the automated command or standard Django createsuperuser:
```bash
python manage.py create_admin
# Default superuser credentials:
# Email: admin@welcometonigeria.com
# Password: adminpass1234
```
Or create a custom administrator:
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 4. Frontend & Backend Integration Details

| Page | Route | Description | Backend Integration |
| :--- | :--- | :--- | :--- |
| **Home** | `/` or `/index.html` | Featured stories, state directory, quotes | `GET /api/stories/?featured=true&limit=3` & `GET /api/states/` |
| **Explore Stories** | `/stories.html` | Real-time search, state filtering, sorting | `GET /api/stories/?q=...&state=...&sort=...` |
| **Story Detail** | `/story.html?id=<id>` | Long-form story, photo gallery, lightbox, tips, related | `GET /api/stories/<id>/` & `POST /api/stories/<id>/save/` |
| **States** | `/states.html` | All 36 states + FCT Abuja directory | `GET /api/states/` |
| **State Filter** | `/state.html?state=<name>` | Filtered stories by selected state | `GET /api/stories/?state=<name>` |
| **Share Story** | `/share-story.html` | Multi-image story submission | `POST /api/stories/submit/` (Multipart with photos) |
| **Sign Up** | `/signup.html` | Contributor registration | `POST /api/auth/signup/` |
| **Sign In** | `/signin.html` | Secure session login | `POST /api/auth/signin/` |
| **My Account** | `/account.html` | Contributor dashboard (Pending, Published, Saved) | `GET /api/auth/me/`, `GET /api/stories/user/`, `PATCH /api/auth/profile/` |
| **Traveller Profile**| `/profile.html?id=<user>` | Public contributor profile & stories | `GET /api/auth/profiles/<id>/` |
| **Contact** | `/contact.html` | Inquiries & editorial questions | `POST /api/interactions/contact/` |
| **Newsletter** | Global footer on all pages | Email updates subscription | `POST /api/interactions/newsletter/` |
| **Django Admin** | `/admin/` | Story review, publishing, and content moderation | Built-in Django Admin with bulk approval actions |

---

## 5. Editorial Moderation Workflow

1. When a contributor or guest submits a story via `share-story.html`, it is created in the database with status `pending` (**Pending Review**).
2. The submission is immediately visible to the logged-in author in their account dashboard under **My Stories** and the **Pending** tab.
3. The story remains hidden from public listings until reviewed.
4. An editor logs into `/admin/` -> **Stories** -> selects the pending submissions -> chooses **Approve and Publish selected stories** from the actions menu.
5. The story is marked `published` with today's publication date and immediately appears across public story feeds, state pages, and featured slots.

---

## 6. Running Tests

Execute the comprehensive automated test suite:
```bash
python manage.py test
```
All 16 test cases cover models, API endpoints, authentication flows, story submissions with image uploads, and page rendering with CSRF validation.

---

## 7. Production Deployment Instructions

1. **Database**: Provide a production PostgreSQL database URL via `DATABASE_URL` in `.env` (e.g. `postgres://user:password@hostname:5432/wtn_db`).
2. **Secret Key & Debug**: Set `SECRET_KEY` to a cryptographically secure string and `DEBUG=False` in `.env`.
3. **Allowed Hosts & CSRF**: Add your domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
4. **Static Files**: Run `python manage.py collectstatic --noinput`. WhiteNoise handles compressed, cache-busted static files automatically.
5. **WSGI Server**: Run using Gunicorn:
   ```bash
   gunicorn wtn_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```
6. **Reverse Proxy (Nginx/Caddy)**: Configure Nginx or Caddy to proxy requests to `http://127.0.0.1:8000`, configure SSL/TLS (Let's Encrypt), and point `/media/` to the media directory if offloading media serving.

