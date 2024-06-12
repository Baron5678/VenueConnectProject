"""
URL configuration for VenueConnectProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView

from VenueConnect import views

urlpatterns = [
    re_path(r'^(?P<url>.+)\.html$', RedirectView.as_view(url='/%(url)s', permanent=True)),
    path('', views.home_view, name='home'),
    path('register.html/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('verify_email_confirm/<uidb64>/<token>/', views.verify_email_confirm, name='verify_email_confirm'),
    path('users/<userid>/', views.UsersView.as_view(), name='users'),
    path('users/<userid>/profile/', views.ProfileView.as_view(), name='profile'),
    path('users/<userid>/advertisements/', views.AdvertisementsView.as_view(), name='advertisements'),
    path('users/<userid>/bookings/', views.BookingsView.as_view(), name='bookings'),
    path('users/<userid>/bookings/<booking_id>', views.BookingView.as_view(), name='booking'),
    path('users/<userid>/advertisements/<ad_id>/', views.AdvertisementView.as_view(), name='advertisement'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('404', views.not_found_view, name='not_found'),
   # path('create-venue/', views.create_venue, name='create_venue'),
]
