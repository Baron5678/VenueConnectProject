import random

from django.core.management.base import BaseCommand
from faker import Faker

import VenueConnect.models as models


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        faker = Faker()
        for _ in range(3):
            models.User.register(
                faker.user_name(),
                faker.email(),
                faker.password(length=20),
                faker.first_name(),
                faker.last_name(),
                faker.random_int(),
            )

        for _ in range(5):
            models.Venue.objects.create(
                venueName=faker.name(),
                address=faker.address(),
                capacity=faker.random_int(),
                owner=random.choice(models.User.objects.all()),
                venueType=random.choice([choice[0] for choice in models.Venue.VenueType.choices])
            )

        for _ in range(4):
            models.Review.objects.create(
                venue=random.choice(models.Venue.objects.all()),
                review=faker.text()
            )

        for _ in range(3):
            models.BookingOrder.objects.create(
                bookingDate=faker.date_time_this_year(),
                venue=random.choice(models.Venue.objects.all()),
                user=random.choice(models.User.objects.all())
            )

        for _ in range(5):
            models.Advertisement.objects.create(
                title=faker.sentence(),
                description=faker.text(),
                owner=random.choice(models.User.objects.all()),
                is_active=faker.boolean(),
                venue=random.choice(models.Venue.objects.all())
            )
