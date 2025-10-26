from django.urls import path
from .views import home, pending_users, approve_user, user_logout, user_login, register
from .api_views import UserRegistrationView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Regular Django views
    path('', home, name='home'),  # Home page
    path('pending-users/', pending_users, name='pending_users'),  # Admin approval page
    path('approve-user/<int:user_id>/<str:action>/', approve_user, name='approve_user'),  # Approve/Reject users
    path('logout/', user_logout, name='logout'),  # Logout
    path('login/', user_login, name='login'),  # Login
    path('register/', register, name='register'),  # Register

    # API endpoints
    path('api/auth/register/', UserRegistrationView.as_view(), name='api_register'),  # API registration
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='api_login'),  # API login
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT
]
