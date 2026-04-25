import uuid
import qrcode
import io
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from django.urls import reverse
from events.models import Event


def generate_booking_id():
    return 'BKT-' + str(uuid.uuid4()).upper()[:12]


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('vip', 'VIP'),
        ('platinum', 'Platinum'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booking_id = models.CharField(max_length=20, unique=True, default=generate_booking_id)
    qty = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    booking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f'{self.booking_id} — {self.user.get_full_name()} — {self.event.name}'

    def generate_qr(self):
        """Generate QR code containing a full verification URL"""
        verify_url = reverse('verify_qr', kwargs={'booking_id': self.booking_id})
        data = f"{settings.SITE_URL}{verify_url}"
        qr_img = qrcode.make(data)
        buf = io.BytesIO()
        qr_img.save(buf, format='PNG')
        buf.seek(0)
        filename = f'{self.booking_id}.png'
        self.qr_code.save(filename, File(buf), save=False)  # save=False to avoid recursion

    def calculate_totals(self):
        self.subtotal = self.unit_price * self.qty
        self.booking_fee = round(self.subtotal * Decimal('0.02'), 2)
        self.gst = round(self.subtotal * Decimal('0.18'), 2)
        self.total_amount = self.subtotal + self.booking_fee + self.gst
