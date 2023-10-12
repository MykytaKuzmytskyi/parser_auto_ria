from django.db import models


class Card(models.Model):
    url = models.URLField(primary_key=True, null=False)
    title = models.CharField(max_length=255)
    price_usd = models.IntegerField()
    odometer = models.IntegerField()
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    image_url = models.ImageField()
    images_count = models.IntegerField()
    car_number = models.CharField(max_length=255, null=True)
    car_vin = models.CharField(max_length=255, null=True)
    datetime_found = models.DateTimeField(auto_now_add=True)
