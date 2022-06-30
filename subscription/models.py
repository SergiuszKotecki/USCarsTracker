from django.db import models


# Create your models here.
class EmailSubscription(models.Model):
    first_name = models.CharField(max_length=50)
    email = models.EmailField()

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
