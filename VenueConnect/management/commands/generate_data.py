import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

import VenueConnect.models as models


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # recreate the database
        # self.stdout.write('Resetting the database')
        # call_command('flush', '--no-input', verbosity=0)
        # call_command('makemigrations', verbosity=0)
        # call_command('migrate', verbosity=0)
        self.stdout.write('Creating admin user. Username: admin Password: admin')
        models.User.objects.create_superuser('admin', 'admin@admin', 'admin')
        self.stdout.write('Creating normal user John Doe. Username: user1 Password: password')
        models.User.register('user1', 'user1@users.com', 'password', 'John', 'Doe')

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
                venue_name=faker.name(),
                address=faker.address(),
                capacity=faker.random_int(),
                owner=random.choice(models.User.objects.all()),
                venue_type=random.choice([choice[0] for choice in models.VenueType])
            )

        for _ in range(4):
            models.Review.objects.create(
                venue=random.choice(models.Venue.objects.all()),
                review=faker.text(),
                author=random.choice(models.User.objects.all())
            )

        for _ in range(3):
            time1 = faker.date_time_this_year(tzinfo=timezone.get_current_timezone())
            time2 = faker.date_time_this_year(tzinfo=timezone.get_current_timezone())
            models.BookingOrder.objects.create(
                start_time=min(time1, time2),
                end_time=max(time1, time2),
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
