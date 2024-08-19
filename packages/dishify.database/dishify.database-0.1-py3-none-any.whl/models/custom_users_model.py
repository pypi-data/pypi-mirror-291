from django.contrib.auth.models import AbstractUser
from django.db import models

from .restaurants_model import Restaurants


class CustomUser(AbstractUser):
    restaurants = models.ManyToManyField(Restaurants, db_table="user_restaurants")
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        db_table = "custom_users"


__all__ = ["CustomUser"]
