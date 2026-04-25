import razorpay
import hmac
import hashlib
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bookings.models import Booking
from bookings.utils import send_ticket_email
from .models import Transaction

logger = logging.getLogger(__name__)

# Initialize Razorpay client
try:
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
except Exception as e:
    logger.error(f"Failed to initialize Razorpay client: {e}")
    client = None


@login_required
def create_order(request, booking_id):
    """Create a Razorpay order for the booking."""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if booking.is_paid:
        return JsonResponse({'success': False, 'error': 'Already paid'}, status=400)

    if not client:
        return JsonResponse({'success': False, 'error': 'Payment gateway unavailable'}, status=503)

    amount_paise = int(booking.total_amount * 100)  # Convert to paise

    try:
        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': booking.booking_id,
            'notes': {
                'event': booking.event.name,
                'user_email': request.user.email,
            }
        })

        booking.razorpay_order_id = order['id']
        booking.save()

        # Log pending transaction
        Transaction.objects.create(
            booking=booking,
            razorpay_order_id=order['id'],
            amount=booking.total_amount,
            status='pending'
        )

        return JsonResponse({
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,
            'name': 'BookTix',
            'description': f'{booking.event.name} — {booking.qty}x {booking.category.upper()}',
            'prefill': {
                'name': request.user.get_full_name(),
                'email': request.user.email,
            }
        })
    except Exception as e:
        logger.error(f"Error creating Razorpay order: {e}")
        return JsonResponse({'success': False, 'error': 'Failed to initiate payment'}, status=500)


@csrf_exempt
def payment_callback(request):
    """Handle Razorpay payment callback and verify signature."""
    if request.method != 'POST':
        return HttpResponseBadRequest()

    data = request.POST
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_signature = data.get('razorpay_signature')

    # Find booking and pending transaction
    try:
        booking = Booking.objects.get(razorpay_order_id=razorpay_order_id)
        txn = Transaction.objects.get(razorpay_order_id=razorpay_order_id)
    except (Booking.DoesNotExist, Transaction.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Invalid order ID'}, status=404)

    # Verify signature
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        
        # Update booking
        booking.razorpay_payment_id = razorpay_payment_id
        booking.razorpay_signature = razorpay_signature
        booking.is_paid = True
        booking.status = 'confirmed'
        
        # Reserve seats and generate QR
        booking.event.book_seats(booking.qty)
        booking.generate_qr()
        booking.save()

        # Update transaction
        txn.razorpay_payment_id = razorpay_payment_id
        txn.razorpay_signature = razorpay_signature
        txn.status = 'success'
        txn.save()

        # Send confirmation email
        send_ticket_email(booking)

        return redirect('payment_success', booking_id=booking.booking_id)

    except Exception as e:
        logger.error(f"Payment verification failed: {e}")
        txn.status = 'failed'
        txn.error_message = str(e)
        txn.save()
        return redirect('payment_failed')


@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if not booking.is_paid:
        return redirect('event_list')
    return render(request, 'payments/success.html', {'booking': booking})


@login_required
def payment_failed(request):
    return render(request, 'payments/failed.html')

