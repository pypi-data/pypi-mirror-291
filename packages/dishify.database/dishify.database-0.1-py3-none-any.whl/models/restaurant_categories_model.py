from django.db import models

from .restaurants_model import Restaurants


class RestaurantCategories(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    restaurant = models.ForeignKey(
        Restaurants, on_delete=models.CASCADE, related_name="restaurants_categories"
    )

    class Meta:
        db_table = "restaurant_categories"


__all__ = ["RestaurantCategories"]
