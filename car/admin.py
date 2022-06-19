from django.contrib import admin

# Register your models here.
from car import models


class CarAdmin(admin.ModelAdmin):
    list_display = [
        "make",
        "model",
        "VIN",
        "odometer_mi",
        "odometer_km",
        "run_and_drive",
    ]
    list_filter = ("make", "model")


admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CopartCar, CarAdmin)
admin.site.register(models.IAAICar, CarAdmin)
