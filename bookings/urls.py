from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('checkout/<str:booking_id>/', views.booking_checkout, name='booking_checkout'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<str:booking_id>/', views.ticket_detail, name='ticket_detail'),
    path('verify/<str:booking_id>/', views.verify_qr, name='verify_qr'),
]
