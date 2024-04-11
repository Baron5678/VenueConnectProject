from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .utils import email_verification_token
from .serializers import UserRegistrationSerializer
from .forms import RegisterForm


def index(request):
    return render(request, 'index.html')


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


class AuthViewSet(ViewSet):

    @staticmethod
    def register_form(request):
        next = request.GET.get('next')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('/')

    @staticmethod
    def register_api(request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Process the validated data (e.g., create user)
            # For demonstration, returning a success response
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            User.register(username=username, email=email, password=password)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def register_render(request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    @action(detail=False, methods=['post', 'get'])
    def register(self, request):
        if request.method == 'GET':
            return self.register_render(request)
        if request.content_type == 'application/x-www-form-urlencoded':
            return self.register_form(request)
        if request.content_type == 'application/json':
            return self.register_api(request)
        return Response({"message": "Unknown request source"}, status=400)

    @staticmethod
    def login_render(request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    @staticmethod
    def login_form(request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('/', status.HTTP_200_OK)
        return redirect('/', status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post', 'get'])
    def login(self, request):
        if request.method == 'GET':
            return self.login_render(request)
        if request.content_type == 'application/x-www-form-urlencoded':
            return self.login_form(request)
        return Response({"message": "Unknown request source"}, status=status.HTTP_400_BAD_REQUEST)
