from django.db import models


class TimeRange:
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Calendar:
    reserved_times = []

    def add_reserved_time(self, reserved_time):
        self.reserved_times.append(reserved_time)
