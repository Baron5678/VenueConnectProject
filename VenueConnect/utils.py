from django.db import models
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TimeRange:
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Calendar:
    reserved_times = []

    def add_reserved_time(self, reserved_time):
        self.reserved_times.append(reserved_time)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.email_verified)
        )


email_verification_token = TokenGenerator()