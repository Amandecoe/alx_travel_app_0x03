# 🧳 ALX Travel Booking App

A Django-based travel booking system that allows users to browse trips, make bookings, and receive booking confirmation emails asynchronously using Celery + Redis.

## ✨ Features

### 🔑 User authentication & registration

### 🏝️ Manage trips (CRUD for destinations, prices, schedules)

### 📖 Book trips with instant booking confirmation

### 📧 Asynchronous booking confirmation emails (Celery + Django email backend)

### ⚡ RESTful API powered by Django REST Framework

### 🗄️ Data stored in SQLite/PostgreSQL (configurable)

## 🛠️ Tech Stack

### Backend: Django, Django REST Framework

### Async Tasks: Celery with Redis as the message broker

### Database: SQLite (dev), PostgreSQL (prod)

### Email: Django Email Backend (SMTP or console backend for local testing)

### Deployment Ready: Gunicorn/Daphne + Nginx (optional)

## 📂 Project Structure
```
alx_travel_app_0x03/
│
├── alx_travel_app/        # Main project settings
│   ├── __init__.py        # Celery app loaded here
│   ├── celery.py          # Celery config
│   ├── settings.py        # Django settings (includes Celery + Email)
│   ├── urls.py
│
├── bookings/              # Booking app
│   ├── models.py          # Booking model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # BookingViewSet (triggers email task)
│   ├── tasks.py           # Celery tasks (send booking confirmation email)
│
├── manage.py
└── requirements.txt
```
## ⚙️ Setup Instructions
### 1. Clone repo
```bash
git clone https://github.com/yourusername/alx_travel_app.git
cd alx_travel_app_0x03
```
### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate    # On Linux/macOS
venv\Scripts\activate       # On Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Configure environment

In settings.py, configure your email backend:

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # dev
# or SMTP for real emails


### Make sure Redis is installed and running:
``` bash
redis-server
```
### 5. Run migrations
```bash
python manage.py migrate
```
### 6. Start Django server
``` bash
python manage.py runserver
```
### 7. Start Celery worker
``` bash
celery -A alx_travel_app worker -l info
```
📬 Sending Confirmation Emails

When a user books a trip, BookingViewSet triggers:

send_booking_confirmation_email.delay(user_email, booking_id)


Celery queues the task and sends the email via Django’s email backend.

## 🧪 Testing

Create a booking via API (e.g., POST /bookings/).
Check your console (if using console backend) or inbox (if using SMTP).

## 🚀 Deployment

Use Gunicorn or Daphne for Django

Use Supervisor or systemd to run Celery workers in background

Use Redis or RabbitMQ in production for reliability

## 🤝 Contributing

PRs welcome! Please open an issue first to discuss major changes.

📄 License

MIT License — free to use and modify.
