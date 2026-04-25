from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_ticket_email(booking):
    """
    Sends a confirmation email with the ticket details and QR code link.
    """
    subject = f'Your Ticket for {booking.event.name} is Confirmed!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = booking.user.email

    # Context for the template
    context = {
        'booking': booking,
        'user_name': booking.user.get_full_name() or booking.user.username,
        'site_url': 'http://127.0.0.1:8000',  # Replace with actual domain in production
    }

    # Render HTML and plain text versions
    html_content = render_to_string('bookings/emails/ticket_confirmation.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
