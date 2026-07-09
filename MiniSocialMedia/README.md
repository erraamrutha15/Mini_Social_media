# ✦ MiniSocial — Mini Social Media Platform

A beautifully crafted, full-stack mini social media application built with **Django REST Framework** (backend) and **Vanilla JavaScript** (frontend). MiniSocial features a premium dark-themed glassmorphism UI with smooth animations, letting users connect, share, and engage.

---

## 🚀 Features

- **User Authentication** — Register and login with secure token-based authentication
- **User Profiles** — View and edit your profile with bio, name, follower/following counts
- **Posts Feed** — Create, view, and delete posts in a beautiful social feed
- **Likes** — Like and unlike posts with animated heart interactions
- **Comments** — Add comments to any post with real-time updates
- **Follow System** — Follow and unfollow other users
- **Discover People** — Browse and discover other users on the platform
- **Responsive Design** — Fully responsive across mobile, tablet, and desktop
- **Premium UI** — Dark theme with glassmorphism, gradient accents, and micro-animations

---

## 🛠 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Django 4.2, Django REST Framework |
| Frontend   | HTML5, CSS3, Vanilla JavaScript   |
| Database   | SQLite (default)                  |
| Auth       | Token-based (DRF TokenAuth)       |
| Styling    | Custom CSS with CSS Variables, Glassmorphism |
| Font       | Inter (Google Fonts)              |

---

## 📁 Folder Structure

```
MiniSocialMedia/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── social_media/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── posts/
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── admin.py
├── frontend/
│   ├── index.html
│   ├── feed.html
│   ├── profile.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── README.md
└── requirements.txt
```

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.8+** installed
- A modern web browser (Chrome, Firefox, Edge, Safari)

### Step-by-Step Instructions

1. **Clone or download** the project:
   ```bash
   git clone <repository-url>
   cd mini_social_media_platform/MiniSocialMedia
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

5. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Create database migrations**:
   ```bash
   python manage.py makemigrations accounts posts
   ```

7. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

8. **Create a superuser** (optional, for Django admin):
   ```bash
   python manage.py createsuperuser
   ```

9. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

10. **Open the frontend** — Open `frontend/index.html` in your browser:
    - Navigate to the file directly, or
    - Use a local server (e.g., VS Code Live Server extension)

> **Note**: The backend runs on `http://127.0.0.1:8000` by default. CORS is configured to allow requests from the frontend.

---

## 🔄 Project Workflow

1. **Register** a new account on the landing page
2. **Sign in** to access the Feed and Profile pages
3. **Create posts** from the Feed page — share your thoughts!
4. **Like & Comment** on posts from the Feed
5. **Visit profiles** — click on usernames to see their profiles
6. **Follow/Unfollow** users from their profile pages
7. **Edit your profile** — update your bio, first name, and last name
8. **Discover** new users from the sidebar on the Profile page

---

## 📸 Screenshots

> Screenshots of the application will be added here.

| Page       | Description              |
|------------|--------------------------|
| Landing    | Hero section with login/register forms |
| Feed       | Social feed with posts, likes, and comments |
| Profile    | User profile with stats, posts, and edit form |

---

## 📄 API Endpoints

| Method | Endpoint                         | Description              |
|--------|----------------------------------|--------------------------|
| POST   | `/api/accounts/register/`        | Register new user        |
| POST   | `/api/accounts/login/`           | Login user               |
| GET    | `/api/accounts/users/`           | List all users           |
| GET    | `/api/accounts/profile/<username>/` | Get user profile      |
| PUT    | `/api/accounts/profile/<username>/` | Update own profile    |
| POST   | `/api/accounts/follow/`          | Follow a user            |
| POST   | `/api/accounts/unfollow/`        | Unfollow a user          |
| GET    | `/api/posts/`                    | List all posts           |
| POST   | `/api/posts/`                    | Create a post            |
| DELETE | `/api/posts/<id>/`               | Delete own post          |
| POST   | `/api/posts/<id>/comments/`      | Add comment to post      |
| POST   | `/api/posts/<id>/like/`          | Like a post              |
| POST   | `/api/posts/<id>/unlike/`        | Unlike a post            |

---

## 📝 License

This project is created for educational purposes. Feel free to use, modify, and distribute.

---

<p align="center">
  <strong>✦ MiniSocial</strong> — Built with passion.
</p>
