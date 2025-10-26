from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser as User
from .forms import CustomUserCreationForm

# ----------------------
# Home Page
# ----------------------
def home(request):
    """
    Landing page for AirBooking.
    Shows Register/Login/Admin Login buttons or user info if logged in.
    """
    return render(request, 'users/home.html')

# ----------------------
# Admin Check Decorator
# ----------------------
def admin_required(view_func):
    """
    Decorator to restrict access to staff/admin users only.
    """
    decorated_view_func = user_passes_test(lambda u: u.is_staff, login_url='/')(view_func)
    return decorated_view_func

# ----------------------
# Pending Users
# ----------------------
@login_required
@admin_required
def pending_users(request):
    """
    Display all users with approval_status='Pending'.
    Only accessible by admin/staff.
    """
    pending_users_list = User.objects.filter(approval_status='Pending')
    context = {'pending_users': pending_users_list}
    return render(request, 'users/pending_users.html', context)

# ----------------------
# Approve/Reject User
# ----------------------
@login_required
@admin_required
def approve_user(request, user_id, action):
    """
    Approve or reject a pending user.
    'action' should be either 'approve' or 'reject'.
    """
    user = get_object_or_404(User, id=user_id)

    if action.lower() == 'approve':
        user.approval_status = 'Approved'
        messages.success(request, f"User '{user.username}' approved successfully.")
    elif action.lower() == 'reject':
        user.approval_status = 'Rejected'
        messages.success(request, f"User '{user.username}' rejected successfully.")
    else:
        messages.error(request, "Invalid action.")

    user.save()
    return redirect('pending_users')

# ----------------------
# Logout
# ----------------------
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# ----------------------
# Login (approved users only)
# ----------------------
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_approved():
                    login(request, user)
                    messages.success(request, f"Welcome {user.username}!")
                    return redirect('home')
                else:
                    messages.error(request, "Your account is not approved yet.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# ----------------------
# Registration
# ----------------------
def register(request):
    """
    Handles user registration.
    Creates a user with approval_status='Pending' by default.
    Shows success or error messages.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Wait for admin approval.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)
