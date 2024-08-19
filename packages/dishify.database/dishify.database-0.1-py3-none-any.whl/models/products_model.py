from django.db import models

from .allergens_model import Allergens
from .combo_ingredients_section_model import ComboIngredientsSections
from .extra_ingredients_model import ExtraIngredients
from .removable_ingredients_model import RemovableIngredients
from .restaurant_categories_model import RestaurantCategories
from .restaurants_model import Restaurants


class Products(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    net_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300)
    img = models.CharField(max_length=255, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    enabled = models.BooleanField(default=True)

    restaurant = models.ForeignKey(
        Restaurants, on_delete=models.CASCADE, related_name="restaurants"
    )
    allergens = models.ManyToManyField(Allergens, db_table="product_allergen")
    category = models.ForeignKey(
        RestaurantCategories,
        on_delete=models.CASCADE,
        related_name="restaurant_categories",
    )
    extra_ingredients = models.ManyToManyField(
        ExtraIngredients, db_table="product_extra-ingredients"
    )
    removable_ingredients = models.ManyToManyField(
        RemovableIngredients, db_table="product_removable-ingredients"
    )
    combo_ingredients_sections = models.ManyToManyField(
        ComboIngredientsSections, db_table="product_combo-ingredients"
    )

    class Meta:
        db_table = "products"


__all__ = ["Products"]
