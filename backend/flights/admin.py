from django.contrib import admin
from .models import Flight, Booking

# Flight admin
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        'flight_number',
        'departure_airport',
        'arrival_airport',
        'departure_datetime',
        'arrival_datetime',
        'price',
        'seats_available',
        'status'
    )
    list_filter = ('status', 'departure_airport', 'arrival_airport')
    search_fields = ('flight_number', 'departure_airport', 'arrival_airport')


# Booking admin
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'flight',
        'seats_booked',      # matches model
        'booked_at',         # matches model
        'payment_status'
    )
    list_filter = ('payment_status',)
    search_fields = ('user__username', 'flight__flight_number')


# Register models with admin
admin.site.register(Flight, FlightAdmin)
admin.site.register(Booking, BookingAdmin)
