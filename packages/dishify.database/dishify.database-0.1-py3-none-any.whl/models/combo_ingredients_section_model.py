from django.db import models

from .combo_ingredients_model import ComboIngredients


class ComboIngredientsSections(models.Model):
    name = models.CharField(max_length=255)
    max_use = models.IntegerField()
    ingredients = models.ManyToManyField(
        ComboIngredients, related_name="combo_ingredients_sections_ingredients"
    )

    class Meta:
        db_table = "combo_ingredients_sections"


__all__ = ["ComboIngredientsSections"]
