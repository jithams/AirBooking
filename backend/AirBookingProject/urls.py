# AirBookingProject/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import home  # Home page view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # -------------------------------
    # Admin panel
    # -------------------------------
    path('admin/', admin.site.urls),

    # -------------------------------
    # Frontend / App routes
    # -------------------------------
    path('', home, name='home'),                # Home page
    path('users/', include('users.urls')),      # Users app pages (login/register if any)
    path('flights/', include('flights.urls')),  # Flights app pages

    # -------------------------------
    # REST API routes
    # -------------------------------
    path('api/users/', include('users.api_urls')),       # Users API
    path('api/flights/', include('flights.api_urls')),   # Flights API

    # -------------------------------
    # JWT Authentication endpoints
    # -------------------------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access & refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh access token
]
