# BookTix — Django Event Ticket Booking System

A full-featured event ticket booking platform built with Django, Razorpay payment integration, and QR code-based entry verification.

---

## Quick Start

### 1. Clone / Extract the project
```
cd booktix/
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Razorpay keys
Open `booktix/settings.py` and replace:
```python
RAZORPAY_KEY_ID     = 'rzp_test_YOUR_KEY_ID'
RAZORPAY_KEY_SECRET = 'YOUR_KEY_SECRET'
```
Get your keys from https://dashboard.razorpay.com

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Project Structure

```
booktix/
├── manage.py
├── requirements.txt
├── README.md
├── booktix/               # Project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events/                # Event browsing
│   ├── models.py          # Event, Category
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/events/
│       ├── event_list.html
│       └── event_detail.html
├── bookings/              # Ticket booking + QR
│   ├── models.py          # Booking (with QR generation)
│   ├── views.py           # Book, checkout, verify QR
│   ├── urls.py
│   ├── admin.py
│   └── templates/bookings/
│       ├── book.html
│       ├── checkout.html
│       ├── my_tickets.html
│       └── ticket_detail.html
├── payments/              # Razorpay integration
│   ├── views.py           # create_order, callback, success
│   ├── urls.py
│   └── templates/payments/
│       ├── success.html
│       └── failed.html
├── users/                 # Auth + profiles
│   ├── models.py          # UserProfile
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/users/
│       ├── login.html
│       ├── register.html
│       └── profile.html
├── templates/
│   └── base.html          # Shared base template
├── static/
│   ├── css/style.css      # All styles
│   └── js/main.js         # All JavaScript
└── media/
    └── qrcodes/           # Generated QR images
```

---

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | event_list | Browse all events |
| `/event/<id>/` | event_detail | Event details page |
| `/auth/register/` | register_view | User registration |
| `/auth/login/` | login_view | User login |
| `/auth/logout/` | logout_view | Logout |
| `/auth/profile/` | profile_view | User profile |
| `/bookings/book/<event_id>/` | book_event | Select tickets |
| `/bookings/checkout/<booking_id>/` | booking_checkout | Payment page |
| `/bookings/my-tickets/` | my_tickets | View all bookings |
| `/bookings/ticket/<booking_id>/` | ticket_detail | Printable QR ticket |
| `/bookings/verify/<booking_id>/` | verify_qr | QR verification API |
| `/payment/create-order/<booking_id>/` | create_order | Razorpay order API |
| `/payment/callback/` | payment_callback | Razorpay webhook |
| `/payment/success/<booking_id>/` | payment_success | Success page |
| `/admin/` | Django admin | Admin dashboard |

---

## Admin Panel

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Manage: Events, Categories, Bookings, Users, Profiles

---

## QR Code Verification

The QR code encodes: `{booking_id}:{user_id}:{event_id}`

To verify at event entry, call:
```
GET /bookings/verify/<booking_id>/
```
Returns JSON:
```json
{"valid": true, "user": "Arjun Rao", "event": "Sunburn 2025", ...}
{"valid": false, "message": "Ticket already used!"}
```

---

## Adding Sample Data

```bash
python manage.py shell
```
```python
from events.models import Category, Event
from django.utils import timezone
import datetime

cat = Category.objects.create(name='Music', icon='🎵', slug='music')
Event.objects.create(
    name='Sunburn Arena 2025',
    description='The biggest music festival in India.',
    date=timezone.now() + datetime.timedelta(days=30),
    venue='HITEX Exhibition Centre',
    city='Hyderabad',
    category=cat,
    price_general=1499,
    price_vip=2499,
    price_platinum=4999,
    total_seats=500,
    available_seats=500,
    is_active=True,
    is_featured=True,
)
```

---

## Technologies Used

- **Backend**: Django 4.2, Python 3.11
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Payment**: Razorpay
- **QR Code**: `qrcode` + `Pillow`
- **Static files**: WhiteNoise

---

## Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Set a strong `SECRET_KEY` via environment variable
- [ ] Configure PostgreSQL database
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure real SMTP email (not console backend)
- [ ] Run `python manage.py collectstatic`
- [ ] Use gunicorn + nginx
