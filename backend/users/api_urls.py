from django.urls import path
from .api_views import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    # User registration API: creates inactive user pending admin approval
    path('register/', UserRegistrationView.as_view(), name='api_register'),

    # JWT login API: only allows active users to obtain token
    path('login/', CustomTokenObtainPairView.as_view(), name='api_login'),
]
