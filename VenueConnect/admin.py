from django.contrib import admin

from .models import User, Venue, Review, BookingOrder, Advertisement

admin.site.register(User)
admin.site.register(Venue)
admin.site.register(Review)
admin.site.register(BookingOrder)
admin.site.register(Advertisement)
