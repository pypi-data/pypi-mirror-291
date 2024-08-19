from django.db import models

from .restaurants_model import Restaurants


class ExtraIngredients(models.Model):
    name = models.CharField(max_length=255)
    max_extra_ingredients = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(
        Restaurants,
        on_delete=models.CASCADE,
        related_name="restaurant_extra_ingredients",
    )

    class Meta:
        db_table = "extra_ingredients"


__all__ = ["ExtraIngredients"]
