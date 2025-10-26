# flights/api_urls.py
from django.urls import path
from .api_views import (
    FlightSearchAPIView, FlightDetailAPIView,
    BookingCreateAPIView, UserBookingsListAPIView, BookingDetailAPIView,
    update_flight_status,
)

urlpatterns = [
    path('search/', FlightSearchAPIView.as_view(), name='api_flight_search'),
    path('<int:pk>/', FlightDetailAPIView.as_view(), name='api_flight_detail'),

    path('bookings/', BookingCreateAPIView.as_view(), name='api_booking_create'),
    path('bookings/my/', UserBookingsListAPIView.as_view(), name='api_my_bookings'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='api_booking_detail'),

    # Admin flight status update
    path('admin/flights/<int:pk>/status/', update_flight_status, name='api_admin_update_flight_status'),
]
