from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'event', 'qty', 'category',
                    'total_amount', 'is_paid', 'is_used', 'status', 'booked_at']
    list_filter = ['status', 'is_paid', 'is_used', 'category']
    search_fields = ['booking_id', 'user__username', 'user__email', 'event__name']
    readonly_fields = ['booking_id', 'razorpay_order_id', 'razorpay_payment_id',
                       'razorpay_signature', 'qr_code', 'booked_at', 'used_at']
    fieldsets = (
        ('Booking Info', {'fields': ('booking_id', 'user', 'event', 'qty', 'category')}),
        ('Pricing', {'fields': ('unit_price', 'subtotal', 'booking_fee', 'gst', 'total_amount')}),
        ('Payment', {'fields': ('razorpay_order_id', 'razorpay_payment_id',
                                'razorpay_signature', 'is_paid')}),
        ('Entry', {'fields': ('is_used', 'used_at', 'qr_code')}),
        ('Status', {'fields': ('status', 'booked_at')}),
    )

    actions = ['mark_as_confirmed', 'mark_as_cancelled']

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = 'Mark selected bookings as Confirmed'

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Mark selected bookings as Cancelled'
