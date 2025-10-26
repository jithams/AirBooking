# flights/serializers.py
from rest_framework import serializers
from .models import Flight, Booking

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ('id',)

class BookingSerializer(serializers.ModelSerializer):
    # flight is specified by its ID on write; read will return id/reference
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    class Meta:
        model = Booking
        fields = ('id', 'user', 'flight', 'seats_booked', 'payment_status', 'booking_date')
        read_only_fields = ('id', 'user', 'booking_date')
