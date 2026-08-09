from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Address
from orders.models import Order
from wishlist.models import Wishlist

def login_view(request):
    """
    User authentication view with password visibility toggle & clean validation.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if username is an email address
        user_obj = User.objects.filter(email=username_or_email).first()
        if user_obj:
            username = user_obj.username
        else:
            username = username_or_email

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'core:home')
        else:
            messages.error(request, "Invalid credentials. Please check your username and password.")

    return render(request, 'accounts/login.html')


def register_view(request):
    """
    User Registration view creating standard Django User and associated UserProfile.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'accounts/register.html')

        # Split full name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)
        messages.success(request, f"Welcome to NexCart, {user.first_name}! Account created successfully.")
        return redirect('core:home')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('core:home')


@login_required
def profile_view(request):
    """
    User Profile View with tabs for Dashboard Overview, Edit Profile, Addresses, Order History, and Security.
    """
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    addresses = Address.objects.filter(user=user)
    orders = Order.objects.filter(user=user).prefetch_related('items', 'tracking_events')
    
    wishlist = Wishlist.objects.filter(user=user).first()
    wishlist_items = wishlist.items.all() if wishlist else []

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.save()
            
            profile.phone = request.POST.get('phone', profile.phone)
            profile.bio = request.POST.get('bio', profile.bio)
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')

        elif action == 'add_address':
            Address.objects.create(
                user=user,
                title=request.POST.get('title', 'Home'),
                full_name=request.POST.get('full_name'),
                phone=request.POST.get('phone'),
                street_address=request.POST.get('street_address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                postal_code=request.POST.get('postal_code'),
                country=request.POST.get('country', 'United States'),
                is_default=request.POST.get('is_default') == 'on'
            )
            messages.success(request, "New shipping address added.")
            return redirect('accounts:profile')

    context = {
        'profile': profile,
        'addresses': addresses,
        'orders': orders,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'accounts/profile.html', context)
