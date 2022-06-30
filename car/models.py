from django.db import models
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    class ColorChoice(models.TextChoices):
        BLACK = 'BK', _('Black')
        WHITE = 'WE', _('White')
        RED = 'RD', _('Red')
        BLUE = 'BE', _('Blue')

    VIN = models.CharField(max_length=17, blank=True, null=True)
    odometer_mi = models.IntegerField(blank=True, null=True)
    odometer_km = models.IntegerField(blank=True, null=True)
    run_and_drive = models.BooleanField(default=False)
    year = models.IntegerField(default=2000, blank=False, null=False)
    make = models.CharField(max_length=20, blank=True, null=True)
    model = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(choices=ColorChoice.choices, default=ColorChoice.BLACK, max_length=2)

    def mi_to_km(self):
        self.odometer_km = int(self.odometer_mi * 1.609344)

    def __str__(self):
        return f"{self.make} {self.model} {self.VIN}"


class CopartCarAuction(models.Model):
    current_bid = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    buy_now = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=False, blank=True, null=True)  # last update for copart data
    auction_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    loot_id = models.CharField(max_length=20, blank=False, null=False, unique=True)

    refresh_data = models.BooleanField(default=True)

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car} {self.auction_date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['car', 'auction_date'], name='Uniqe car and auction date'),
        ]
