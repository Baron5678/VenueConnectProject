from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import Calendar, email_verification_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserManager(BaseUserManager):
    def create_user(self,
                    username,
                    password,
                    first_name,
                    last_name,
                    email,
                    phone_number,
                    **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            **extra_fields)
        user.set_password(password)
        user.email_is_verified = False
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    # By default, django includes:
    # first_name instead of name
    # last_name
    # email

    # we have to extend the model by the phone number:
    phone_number = models.IntegerField(null=True)
    email_verified = models.BooleanField(default=False)

    @staticmethod
    def register(username,
                 password,
                 first_name,
                 last_name,
                 email,
                 phone_number):
        return UserManager().create_user(username=username,
                                         password=password,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email,
                                         phone_number=phone_number)

    def send_verification_email(self, request_scheme, domain):
        subject = "Verify Email"
        message = render_to_string('verify_email_msg.html', {
            'request_scheme': request_scheme,
            'user': self,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': email_verification_token.make_token(self),
        })
        email = EmailMessage(
            subject, message, to=[self.email]
        )
        email.content_subtype = 'html'
        email.send()


class Venue(models.Model):
    class VenueType(models.TextChoices):
        CONCERT_HALL = 'CH', 'Concert Hall'
        SPORTS_ARENA = 'SA', 'Sports Arena'
        THEATER = 'TH', 'Theater'
        CONFERENCE_ROOM = 'CR', 'Conference Room'
        OPEN_AIR = 'OA', 'Open Air'
    venueName = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    venue_type = models.CharField(
        max_length=2,
        choices=VenueType.choices,
        default=VenueType.CONCERT_HALL,
    )
    capacity = models.IntegerField()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_venues'
    )

    availabilityCalendar = Calendar()


class Review(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='review')
    review = models.TextField(max_length=500)


class BookingOrder(models.Model):
    bookingDate = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='booking_order')
    # the spec talks about the 'paymentID' attribute, but since the payment processing
    # has been scrapped, it was skipped
