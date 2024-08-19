from django.db import models

from .combo_sections_model import ComboSections
from .restaurants_model import Restaurants


class Combos(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=300, default="", blank=True)
    image_url = models.CharField(max_length=255, blank=True, default="")
    sections = models.ManyToManyField(
        ComboSections,
        db_column="combo_combo-sections",
        blank=True,
        default=None,
    )
    restaurant = models.ForeignKey(
        Restaurants, on_delete=models.CASCADE, related_name="combos_restaurants"
    )
    active = models.BooleanField(db_column="active", default=True)

    class Meta:
        db_table = "combos"


__all__ = ["Combos"]
