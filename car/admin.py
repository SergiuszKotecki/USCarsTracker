from django.contrib import admin

# Register your models here.
from car import models
from car.models import CopartCarAuction


class AuctionCarAdmin(admin.ModelAdmin):
    list_display = [
        "make",
        "model",
        "VIN",
        "odometer_mi",
        "odometer_km",
        "run_and_drive",
        "loot_id",
    ]
    list_filter = ("make", "model")


admin.site.register(CopartCarAuction)
