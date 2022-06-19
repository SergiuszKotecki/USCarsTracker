from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


def mi_to_km(mi):
    return int(mi * 1.609344)


class Car(models.Model):
    class ColorChoice(models.TextChoices):
        BLACK = 'BK', _('Black')
        WHITE = 'WE', _('White')
        RED = 'RD', _('Red')
        BLUE = 'BE', _('Blue')

    VIN = models.CharField(max_length=17)
    odometer_mi = models.IntegerField(blank=True, null=True)
    odometer_km = models.IntegerField(blank=True, null=True)
    run_and_drive = models.BooleanField(default=False)
    year = models.IntegerField(default=2000, blank=False, null=False)
    make = models.CharField(max_length=20, blank=False, null=False)
    model = models.CharField(max_length=20, blank=False, null=False)
    color = models.CharField(choices=ColorChoice.choices, default=ColorChoice.BLACK, max_length=2)

    def save(self, *args, **kwargs):
        if not self.odometer_km:
            self.odometer_km = mi_to_km(self.odometer_mi)
        super(Car, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.make} {self.model} {self.VIN}"


class CopartCar(Car):
    loot_id = models.IntegerField(blank=False, null=False)


class IAAICar(Car):
    loot_id = models.CharField(max_length=20, blank=False, null=False)


class CarAuction(models.Model):
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    buy_now = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=False, blank=True, null=True)
