# Advanced E-Learning Platform

A comprehensive, production-ready e-learning platform built with **Django 5**, featuring courses, video lessons, quizzes, certificates, payments, real-time notifications, and much more.

![Django](https://img.shields.io/badge/Django-5.0-092E20?style=flat&logo=django)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)
![DRF](https://img.shields.io/badge/DRF-3.14-A30000?style=flat)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-38B2AC?style=flat&logo=tailwind-css)

---

## 🚀 Features

### Core Features
| Feature | Description |
|---------|-------------|
| **User Roles** | Student, Instructor, Admin with role-based permissions |
| **JWT Authentication** | Secure authentication with email verification |
| **Social Login** | Google, GitHub, LinkedIn, Facebook |
| **2FA** | Two-factor authentication via SMS/TOTP |
| **Course Management** | Full CRUD for courses with video lessons |
| **Enrollment System** | Track progress, lesson completion |
| **Quiz System** | MCQ, True/False, Short Answer with auto-grading |
| **Certificates** | PDF generation with verification |
| **Payments** | Stripe integration |
| **Real-time Notifications** | WebSocket notifications |
| **Reviews & Ratings** | Course reviews with aggregation |
| **Search & Filters** | Advanced course search |

### Advanced Features
| Feature | Description |
|---------|-------------|
| **Gamification** | Badges, achievements, leaderboards, points, streaks |
| **Interactive Learning** | Code editor, flashcards, whiteboard |
| **Social Learning** | Discussions, study groups, connections |
| **Personalization** | Learning paths, AI recommendations |
| **Accessibility** | WCAG compliance, accessibility preferences |
| **Analytics** | User behavior tracking, learning analytics |

---

## 📋 Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+, PostgreSQL 15+, Redis 7+

---

## 🛠️ Quick Start with Docker

### 1. Clone and Setup
```bash
cd "e:\coding\company project\group work\Advance django\elearning_platform"
copy env.example .env
```

### 2. Start Services
```bash
docker-compose up --build
```

### 3. Run Migrations & Seed Data
```bash
# In a new terminal
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell < scripts/seed_data.py
```

### 4. Build CSS
```bash
npm install
npm run build:css
```

### 5. Access Application
- **Frontend:** http://localhost
- **Admin:** http://localhost/admin
- **API:** http://localhost/api

---

## 👥 Sample Accounts

After running seed data:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@example.com | admin123 |
| Instructor | instructor@example.com | instructor123 |
| Student | student@example.com | student123 |

---

## 🏗️ Project Structure

```
elearning_platform/
├── apps/
│   ├── users/              # Authentication, profiles, roles
│   ├── courses/            # Course & lesson management
│   ├── enrollment/         # Enrollment & progress tracking
│   ├── quizzes/            # Quiz system with auto-grading
│   ├── certificates/       # PDF certificate generation
│   ├── payments/           # Stripe payment integration
│   ├── notifications/      # Real-time WebSocket notifications
│   ├── reviews/            # Course ratings & reviews
│   ├── gamification/       # Badges, points, leaderboards
│   ├── interactive/        # Code editor, flashcards, whiteboard
│   ├── social/             # Discussions, study groups, connections
│   ├── personalization/    # Learning paths, recommendations
│   ├── accessibility/      # WCAG compliance, accessibility
│   └── analytics/          # User behavior tracking, reports
├── config/                 # Django settings (base, dev, prod)
├── templates/              # Django HTML templates
├── static/                 # Tailwind CSS, JS
├── scripts/                # Data seeding scripts
├── tests/                  # Test suite
├── docker/                 # Docker configs
└── requirements/           # Python dependencies
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register/          # User registration
POST   /api/auth/login/             # JWT login
POST   /api/auth/token/refresh/     # Refresh token
POST   /api/auth/verify-email/      # Verify email
POST   /api/auth/password-reset/    # Password reset
GET    /api/auth/profile/           # User profile
```

### Courses
```
GET    /api/courses/                # List courses
GET    /api/courses/{slug}/         # Course details
POST   /api/courses/                # Create course
GET    /api/courses/categories/     # List categories
GET    /api/courses/{slug}/lessons/ # Course lessons
```

### Enrollment
```
GET    /api/enrollment/             # User enrollments
POST   /api/enrollment/enroll/      # Enroll in course
POST   /api/enrollment/lesson/{id}/progress/  # Update progress
```

### Quizzes
```
GET    /api/quizzes/?course_id={id} # List quizzes
GET    /api/quizzes/{id}/           # Quiz details
POST   /api/quizzes/submit/         # Submit attempt
GET    /api/quizzes/attempts/       # User attempts
```

### Certificates
```
GET    /api/certificates/           # User certificates
POST   /api/certificates/generate/{course_id}/  # Generate
GET    /api/certificates/verify/{id}/  # Verify (public)
```

### Payments
```
POST   /api/payments/create-checkout/  # Create checkout
POST   /api/payments/webhook/          # Stripe webhook
GET    /api/payments/history/          # Payment history
```

### Reviews
```
GET    /api/reviews/?course_id={id}  # List reviews
POST   /api/reviews/create/          # Create review
PUT    /api/reviews/{id}/update/     # Update review
```

### Gamification
```
GET    /api/gamification/badges/         # All badges
GET    /api/gamification/my-badges/      # User badges
GET    /api/gamification/achievements/   # User achievements
GET    /api/gamification/leaderboard/    # Rankings
GET    /api/gamification/streak/         # Learning streak
GET    /api/gamification/dashboard/      # Full dashboard
```

### Social
```
GET    /api/social/discussions/     # List discussions
POST   /api/social/discussions/     # Create discussion
POST   /api/social/discussions/{id}/comments/  # Add comment
GET    /api/social/study-groups/    # List study groups
POST   /api/social/study-groups/{id}/join/     # Join group
```

### Personalization
```
GET    /api/personalization/preferences/     # User preferences
GET    /api/personalization/learning-paths/  # Learning paths
GET    /api/personalization/recommendations/ # Recommendations
POST   /api/personalization/activities/track/ # Track activity
```

### Accessibility
```
GET    /api/accessibility/preferences/    # User preferences
GET    /api/accessibility/features/       # Platform features
POST   /api/accessibility/feedback/       # Submit feedback
GET    /api/accessibility/wcag-summary/   # Compliance summary
```

### Analytics
```
GET    /api/analytics/summary/        # User analytics
GET    /api/analytics/platform/       # Platform stats (admin)
POST   /api/analytics/behavior/track/ # Track behavior
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/users/tests/

# Run with verbose output
pytest -vvs
```

---

## 🎨 Frontend Features

- **Dark Mode** - Toggle between light/dark themes
- **Glassmorphism** - Modern glass-effect UI
- **Responsive** - Mobile-first design
- **Alpine.js** - Lightweight interactivity
- **Tailwind CSS** - Utility-first styling
- **Animations** - Smooth transitions

---

## 🔐 Environment Variables

Key variables in `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=elearning_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

---

## 📚 Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 5.0, Django REST Framework |
| **Database** | PostgreSQL 15 |
| **Cache/Real-time** | Redis, Django Channels |
| **Frontend** | Tailwind CSS, Alpine.js |
| **Authentication** | JWT, django-allauth, 2FA |
| **Payments** | Stripe |
| **PDF** | ReportLab |
| **Containerization** | Docker, Docker Compose |
| **Testing** | pytest, pytest-django |

---

## 🚢 Deployment

### Production Docker Setup

1. Update `.env` for production:
```env
DEBUG=False
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=yourdomain.com
```

2. Build and deploy:
```bash
docker-compose -f docker-compose.yml up -d
```

3. Run migrations:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 📝 Development

### Local Development (Without Docker)

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements/dev.txt

# Set up database
# Create PostgreSQL database: elearning_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed data
python manage.py shell < scripts/seed_data.py

# Build CSS
npm install
npm run watch:css

# Run server
python manage.py runserver
```

---

## 📄 License

This project is for educational purposes.

---

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs.

---

## 📧 Support

For issues or questions, please create an issue in the repository.

---

Built with ❤️ using **Django**, **DRF**, **Channels**, **Tailwind CSS**, and **Alpine.js**
