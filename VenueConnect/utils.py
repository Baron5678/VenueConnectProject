from django.db import models
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime


class TimeRange:
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def includes(self, time):
        return self.start_time <= time <= self.end_time


class Calendar:
    reserved_times = []

    def reserve(self, start_time, end_time):
        self.reserved_times.append(TimeRange(start_time, end_time))

    def check_availability(self, time):
        for time_range in self.reserved_times:
            if time_range.includes(time):
                return False

        return True


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.email_verified)
        )


email_verification_token = TokenGenerator()