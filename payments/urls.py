from django.urls import path
from . import views

urlpatterns = [
    path('create-order/<str:booking_id>/', views.create_order, name='create_order'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('success/<str:booking_id>/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
