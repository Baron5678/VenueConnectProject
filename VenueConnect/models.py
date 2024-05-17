from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .utils import Calendar, email_verification_token, TimeRange


class UserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password,
                    first_name,
                    last_name,
                    phone_number,
                    **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
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

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    @staticmethod
    def register(username,
                 email,
                 password,
                 first_name='',
                 last_name='',
                 phone_number=None):
        return User.objects.create_user(username=username,
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

    def make_booking(self, venue: 'Venue', time: TimeRange):
        if venue.checkAvailability(time):
            self.booking_order = BookingOrder()
            self.booking_order.user = self
            self.booking_order.start_time = time.start_time
            self.booking_order.end_time = time.end_time
            self.booking_order.venue = venue
            self.booking_order.price = venue.reserveVenue(time.start_time, time.end_time)
            self.booking_order.save()
        else:
            return 0

    def cancel_booking(self):
        self.booking_order.delete()

    def browse_venues(self, requested_capacity: int, requested_address: str):
        return Venue.objects.filter(capacity=requested_capacity, address=requested_address)

    def rate_venue(self, chosen_venue: 'Venue', description: str, feedback: int):
        if 10 < feedback < 0:
            return 0
        review = Review()
        review.venue = chosen_venue
        review.author = self
        review.review = description
        review.feedback = feedback
        review.save()

    def message_user(self, subject: str, receiver_email: str, message: str):
        if 5000 < len(message) < 200 and 50 < len(subject) < 1:
            return 0
        email = EmailMessage(subject, message, from_email=self.email, to=receiver_email)
        email.content_subtype = 'html'
        email.send()


class VenueType(models.TextChoices):
    CONCERT_HALL = 'CH', 'Concert Hall'
    SPORTS_ARENA = 'SA', 'Sports Arena'
    THEATER = 'TH', 'Theater'
    CONFERENCE_ROOM = 'CR', 'Conference Room'
    OPEN_AIR = 'OA', 'Open Air'


class Venue(models.Model):
    venueName = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    venueType = models.CharField(
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
    price_per_day = models.IntegerField(default=0)
    availabilityCalendar =  Calendar()

    def checkAvailability(self, time):
        return self.availabilityCalendar.check_availability(time)

    def reserveVenue(self, start_time, end_time):
        days = self.availabilityCalendar.reserve(start_time, end_time)
        self.save()
        return days * self.price_per_day

    def removeVenue(self):
        self.delete()

    def updateVenueDetails(self, *,
                           venueName=None,
                           address=None,
                           venueType=None,
                           capacity=None,
                           owner=None):
        if venueName is not None:
            self.venueName = venueName
        if address is not None:
            self.address = address
        if venueType is not None:
            self.venueType = venueType
        if capacity is not None:
            self.capacity = int(capacity)
        if owner is not None:
            self.owner = owner
        self.save()


class Review(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='review')
    feedback = models.IntegerField(default=0)
    review = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review', default=0)


class BookingOrder(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='booking_order')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_order', default=0)

    # the spec talks about the 'paymentID' attribute, but since the payment processing
    # has been scrapped, it was skipped


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisement')
    is_active = models.BooleanField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='advertisement')
