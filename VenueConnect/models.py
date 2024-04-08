from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from .utils import Calendar


class User(AbstractUser):
    # By default, django includes:
    # first_name instead of name
    # last_name
    # email

    # we have to extend the model by the phone number:
    phone_number = models.IntegerField()
    email_verified = models.BooleanField(default=False)


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
