"""
Template views for user authentication and profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User, Profile


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('student_dashboard' if request.user.is_student else 'instructor_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if not remember_me:
                request.session.set_expiry(0)
            
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect based on user role
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            elif user.is_instructor:
                return redirect('instructor_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth/login.html')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role', 'student')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'auth/signup.html')
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        
        # Auto login after signup
        login(request, user)
        messages.success(request, 'Account created successfully!')
        
        return redirect('student_dashboard' if role == 'student' else 'instructor_dashboard')
    
    return render(request, 'auth/signup.html')


def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile page."""
    return render(request, 'auth/profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })


@login_required
@require_http_methods(["GET", "POST"])
def profile_edit_view(request):
    """Edit user profile."""
    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()
        
        # Update profile fields
        profile = request.user.profile
        profile.bio = request.POST.get('bio', profile.bio)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'auth/profile_edit.html', {
        'user': request.user,
        'profile': request.user.profile
    })
