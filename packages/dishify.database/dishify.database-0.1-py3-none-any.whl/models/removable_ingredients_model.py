from django.db import models

from .restaurants_model import Restaurants


class RemovableIngredients(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(
        Restaurants,
        on_delete=models.CASCADE,
        related_name="restaurant_removable_ingredients",
    )

    class Meta:
        db_table = "removable_ingredients"


__all__ = ["RemovableIngredients"]
