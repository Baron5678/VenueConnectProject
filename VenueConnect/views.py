from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView

from .forms import RegisterForm
from .forms import SignInForm
from .models import User, Advertisement, BookingOrder
from .utils import email_verification_token



def login(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')


def index(request):
    return render(request, 'index.html')

#def create_venue(request):
    # Tu l�gica para crear un lugar aqu�
 #   return render(request, 'create_venue.html')


def not_found_view(request):
    return render(request, '404.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('/')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'verify_email_confirm.html')


class RegisterView(APIView):
    @staticmethod
    def get(request, **kwargs):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form}, **kwargs)

    @staticmethod
    def post(request):
        next = request.GET.get('next')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                if next:
                    return redirect(next)
                else:
                    return redirect('/')
        return render(request, 'register.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @staticmethod
    def get(request, **kwargs):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form}, **kwargs)

    @staticmethod
    def post(request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('/', status.HTTP_200_OK)
            return redirect('/', status.HTTP_401_UNAUTHORIZED)
        return render(request, 'login.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)


def logout_view(self, request, **kwargs):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/', status=status.HTTP_200_OK)
    return redirect('/', status=status.HTTP_401_UNAUTHORIZED)


class UsersView(APIView):
    @staticmethod
    def get(request, userid):
        try:
            user = User.objects.get(pk=userid)
            user = model_to_dict(user)
            return render(request, 'users.html', {'user': user})
        except ObjectDoesNotExist:
            return redirect('/404', status=status.HTTP_404_NOT_FOUND)


class AdvertisementsView(APIView):
    @staticmethod
    def get(request, userid):
        try:
            user = User.objects.get(pk=userid)
            advertisements = Advertisement.objects.filter(owner=user)
            if not advertisements:
                return redirect('/404', status=status.HTTP_404_NOT_FOUND)
            return render(request, 'advertisements.html', {'advertisements': advertisements})
        except ObjectDoesNotExist:
            return redirect('/404', status=status.HTTP_404_NOT_FOUND)


class AdvertisementView(APIView):
    @staticmethod
    def get(request, userid, ad_id):
        try:
            ad = Advertisement.objects.filter(owner_id=userid).get(pk=ad_id)
            return render(request, 'advertisement.html', {'ad': ad})
        except ObjectDoesNotExist:
            return redirect('/404', status=status.HTTP_404_NOT_FOUND)


class BookingsView(APIView):
    @staticmethod
    def get(request, userid):
        try:
            bookings = BookingOrder.objects.filter(user_id=userid).all()
            return render(request, 'bookings.html', {'bookings': bookings})
        except ObjectDoesNotExist:
            return redirect('/404', status=status.HTTP_404_NOT_FOUND)


class BookingView(APIView):
    @staticmethod
    def get(request, userid, booking_id):
        try:
            booking = BookingOrder.objects.filter(user_id=userid).get(pk=booking_id)
            return render(request, 'booking.html', {'booking': booking})
        except ObjectDoesNotExist:
            return redirect('/404', status=status.HTTP_404_NOT_FOUND)
