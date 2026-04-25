from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from events.models import Event
from .models import Booking


@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, is_active=True)

    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))
        category = request.POST.get('category', 'general')

        if qty < 1 or qty > 10:
            return HttpResponseBadRequest("Invalid quantity")

        if event.available_seats < qty:
            return render(request, 'bookings/book.html', {
                'event': event,
                'error': 'Not enough seats available.'
            })

        # Get price based on category
        price_map = {
            'general': event.price_general,
            'vip': event.price_vip,
            'platinum': event.price_platinum,
        }
        unit_price = price_map.get(category, event.price_general)

        booking = Booking(
            user=request.user,
            event=event,
            qty=qty,
            category=category,
            unit_price=unit_price,
        )
        booking.calculate_totals()
        booking.save()

        return redirect('booking_checkout', booking_id=booking.booking_id)

    return render(request, 'bookings/book.html', {'event': event})


@login_required
def booking_checkout(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/checkout.html', {
        'booking': booking,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


@login_required
def my_tickets(request):
    bookings = Booking.objects.filter(user=request.user, is_paid=True)
    return render(request, 'bookings/my_tickets.html', {'bookings': bookings})


@login_required
def ticket_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/ticket_detail.html', {'booking': booking})


def verify_qr(request, booking_id):
    """Verify a QR code at event entry. Supports both JSON and HTML responses."""
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'valid': False, 'message': 'Booking not found.'}, status=404)
        return render(request, 'bookings/verify_result.html', {'valid': False, 'message': 'Booking not found.'}, status=404)

    valid = True
    message = 'Entry allowed!'
    
    if not booking.is_paid:
        valid = False
        message = 'Payment not completed.'
    elif booking.is_used:
        valid = False
        message = f'Ticket already used at {booking.used_at.strftime("%d %b %Y, %I:%M %p")}'
    else:
        # Mark ticket as used only if it's currently valid
        booking.is_used = True
        booking.used_at = timezone.now()
        booking.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'valid': valid,
            'message': message,
            'booking_id': booking.booking_id,
            'user': booking.user.get_full_name(),
            'event': booking.event.name,
            'category': booking.category.upper(),
            'qty': booking.qty,
        })

    return render(request, 'bookings/verify_result.html', {
        'valid': valid,
        'message': message,
        'booking': booking
    })
