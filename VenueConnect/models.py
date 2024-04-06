from django.db import models
from django.conf import settings


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


class Availability(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='availabilities')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()


class Review(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='review')
    review = models.TextField(max_length=500)


class BookingOrder(models.Model):
    bookingDate = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='booking_order')

