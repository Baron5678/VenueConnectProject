from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .utils import email_verification_token
from .serializers import UserRegistrationSerializer


def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signUp.html')


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

    @action(detail=False, methods=['post'])
    def register(self, request):
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
