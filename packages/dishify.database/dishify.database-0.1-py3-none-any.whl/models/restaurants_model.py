from django.db import models


class Restaurants(models.Model):
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255, blank=True, null=True)
    about_us = models.CharField(max_length=300)
    contact_email = models.CharField(max_length=320)
    contact_phone = models.CharField(max_length=15)
    currency = models.CharField(max_length=3)
    main_color = models.CharField(max_length=10, null=True)
    secondary_color = models.CharField(max_length=10, null=True)
    instagram = models.CharField(max_length=255, null=True)
    facebook = models.CharField(max_length=255, null=True)
    twitter = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "restaurants"


__all__ = ["Restaurants"]
