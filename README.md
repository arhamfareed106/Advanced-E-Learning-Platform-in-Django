# Advanced E-Learning Platform

A production-ready e-learning platform built with Django 5, featuring courses, video lessons, quizzes, certificates, payments, and real-time notifications.

## 🚀 Features

### Core Features
- **User Roles**: Student, Instructor, Admin with role-based permissions
- **JWT Authentication**: Secure authentication with email verification and password reset
- **Course Management**: Full CRUD for courses with video lessons, documents, and chapter ordering
- **Enrollment System**: Track progress, lesson completion, and course completion
- **Video Player**: Modern player with autoplay and mark as complete
- **Quiz System**: MCQ, True/False, Short Answer with auto-grading and timer
- **Certificates**: PDF generation with ReportLab and public verification
- **Payments**: Stripe integration for one-time purchases and subscriptions
- **Real-time Notifications**: WebSocket notifications with Django Channels
- **Reviews & Ratings**: Course reviews with automatic rating aggregation
- **Search & Filters**: Advanced course search with category, price, and difficulty filters

### Technical Features
- **REST API**: Full REST API with DRF for all features
- **WebSocket**: Real-time notifications using Django Channels
- **Premium UI**: Tailwind CSS with glassmorphism, dark mode, and animations
- **Responsive**: Mobile-first responsive design
- **Docker**: Complete Docker setup with PostgreSQL, Redis, and Nginx
- **Testing**: Comprehensive test suite with pytest

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for Tailwind CSS)
- Python 3.11+ (if running without Docker)
- PostgreSQL 15+ (if running without Docker)

## 🛠️ Quick Start with Docker

1. **Clone the repository**
   ```bash
   cd "e:\coding\company project\group work\Advance django\elearning_platform"
   ```

2. **Copy environment file**
   ```bash
   copy env.example .env
   ```

3. **Build and start services**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations and seed data** (in a new terminal)
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python scripts/seed_data.py
   ```

5. **Build Tailwind CSS**
   ```bash
   npm install
   npm run build:css
   ```

6. **Access the application**
   - Frontend: http://localhost
   - Admin: http://localhost/admin
   - API: http://localhost/api

## 👥 Sample Accounts

After running the seed data script:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Instructor | instructor | instructor123 |
| Student | student | student123 |

## 🏗️ Project Structure

```
elearning_platform/
├── apps/
│   ├── users/          # User authentication and profiles
│   ├── courses/        # Course and lesson management
│   ├── enrollment/     # Enrollment and progress tracking
│   ├── quizzes/        # Quiz system with auto-grading
│   ├── certificates/   # PDF certificate generation
│   ├── payments/       # Stripe payment integration
│   ├── notifications/  # Real-time notifications
│   └── reviews/        # Course reviews and ratings
├── config/             # Django settings
├── templates/          # Django templates
├── static/             # Static files (CSS, JS, images)
├── docker/             # Docker configuration
├── scripts/            # Utility scripts
└── requirements/       # Python dependencies
```

## 🔧 Local Development (Without Docker)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements/dev.txt
   npm install
   ```

3. **Set up PostgreSQL**
   - Create database: `elearning_db`
   - Update `.env` with database credentials

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed sample data**
   ```bash
   python scripts/seed_data.py
   ```

7. **Build Tailwind CSS**
   ```bash
   npm run watch:css
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/users/tests/
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - JWT login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/verify-email/` - Verify email
- `POST /api/auth/password-reset/` - Request password reset
- `GET /api/auth/profile/` - Get user profile

### Course Endpoints
- `GET /api/courses/` - List courses (with search & filters)
- `GET /api/courses/{slug}/` - Get course details
- `POST /api/courses/` - Create course (instructor only)
- `GET /api/courses/categories/` - List categories

### Enrollment Endpoints
- `GET /api/enrollment/` - List user enrollments
- `POST /api/enrollment/enroll/` - Enroll in course
- `POST /api/enrollment/lesson/{id}/progress/` - Update lesson progress

### Quiz Endpoints
- `GET /api/quizzes/` - List quizzes
- `GET /api/quizzes/{id}/` - Get quiz with questions
- `POST /api/quizzes/submit/` - Submit quiz attempt
- `GET /api/quizzes/attempts/` - List user attempts

### Certificate Endpoints
- `GET /api/certificates/` - List user certificates
- `POST /api/certificates/generate/{course_id}/` - Generate certificate
- `GET /api/certificates/verify/{id}/` - Verify certificate (public)

### Payment Endpoints
- `POST /api/payments/create-checkout/` - Create Stripe checkout
- `POST /api/payments/webhook/` - Stripe webhook handler
- `GET /api/payments/history/` - Payment history

### Review Endpoints
- `GET /api/reviews/?course_id={id}` - List course reviews
- `POST /api/reviews/create/` - Create review
- `PUT /api/reviews/{id}/update/` - Update review

## 🎨 Frontend Features

- **Dark Mode**: Toggle between light and dark themes
- **Glassmorphism**: Modern glass-effect UI components
- **Animations**: Smooth transitions and micro-animations
- **Responsive**: Mobile-first design with Tailwind CSS
- **Alpine.js**: Lightweight JavaScript framework for interactivity

## 🔐 Environment Variables

Key environment variables (see `env.example` for full list):

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=elearning_db
DB_USER=postgres
DB_PASSWORD=postgres
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## 🚢 Deployment

The project includes Docker configuration for easy deployment:

1. Update `.env` with production settings
2. Set `DEBUG=False`
3. Configure proper `SECRET_KEY`
4. Set up SSL certificates for Nginx
5. Run: `docker-compose -f docker-compose.yml up -d`

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs.

## 📧 Support

For issues or questions, please create an issue in the repository.

---

Built with ❤️ using Django, DRF, Channels, Tailwind CSS, and Alpine.js
# Advanced-E-Learning-Platform-in-Django
