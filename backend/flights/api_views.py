# flights/api_views.py
from rest_framework import generics, permissions, status, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer

# Flight search/list (authenticated)
class FlightSearchAPIView(generics.ListAPIView):
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Flight.objects.all()
        departure = self.request.query_params.get('departure')
        arrival = self.request.query_params.get('arrival')
        date = self.request.query_params.get('date')
        if departure:
            qs = qs.filter(departure_airport__icontains=departure)
        if arrival:
            qs = qs.filter(arrival_airport__icontains=arrival)
        if date:
            qs = qs.filter(departure_time__date=date)
        return qs

# Flight detail
class FlightDetailAPIView(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

# Booking create
class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        flight = serializer.validated_data['flight']
        seats = serializer.validated_data.get('seats_booked', 1)
        if flight.seats_available < seats:
            raise drf_serializers.ValidationError("Not enough seats available.")
        flight.seats_available -= seats
        flight.save()
        serializer.save(user=self.request.user)

# List bookings for the current user
class UserBookingsListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

# Booking detail (user or admin)
class BookingDetailAPIView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        return obj

# Admin: update flight status
@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser])
def update_flight_status(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    status_value = request.data.get('status')
    if not status_value:
        return Response({'detail': 'status field required'}, status=status.HTTP_400_BAD_REQUEST)
    flight.status = status_value
    flight.save()
    return Response(FlightSerializer(flight).data)
