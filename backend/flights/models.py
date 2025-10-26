from django.db import models
from django.conf import settings

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_airport = models.CharField(max_length=50)
    arrival_airport = models.CharField(max_length=50)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    seats_available = models.IntegerField()
    status = models.CharField(max_length=20, default='On-time')  # On-time / Delayed

    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport} → {self.arrival_airport}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)  # Number of seats booked
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='Pending')  # Pending / Paid / Failed

    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"
