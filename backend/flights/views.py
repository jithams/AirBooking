from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Flight, Booking

# ----------------------
# Flight List / Search
# ----------------------
@login_required
def flight_list(request):
    """
    Display all flights or filter by departure/arrival airport.
    """
    flights = Flight.objects.all()

    # Optional filtering
    departure = request.GET.get('departure')
    arrival = request.GET.get('arrival')
    if departure:
        flights = flights.filter(departure_airport__icontains=departure)
    if arrival:
        flights = flights.filter(arrival_airport__icontains=arrival)

    return render(request, 'flights/flight_list.html', {'flights': flights})


# ----------------------
# Book Flight
# ----------------------
@login_required
def book_flight(request, flight_id):
    """
    Book a flight for the logged-in user.
    """
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        if seats > flight.seats_available:
            messages.error(request, "Not enough seats available.")
        else:
            Booking.objects.create(
                user=request.user,
                flight=flight,
                seats_booked=seats,
                payment_status='Paid'  # Simulated payment
            )
            flight.seats_available -= seats
            flight.save()
            messages.success(request, f"Booking successful for {flight.flight_number}.")
            return redirect('my_trips')

    return render(request, 'flights/book_flight.html', {'flight': flight})


# ----------------------
# My Trips
# ----------------------
@login_required
def my_trips(request):
    """
    Show all bookings of the logged-in user.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'flights/my_trips.html', {'bookings': bookings})
