# flights/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.flight_list, name='flight_list'),           # Flight search/list
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),  # Book a flight
    path('my-trips/', views.my_trips, name='my_trips'),            # View user bookings
]
