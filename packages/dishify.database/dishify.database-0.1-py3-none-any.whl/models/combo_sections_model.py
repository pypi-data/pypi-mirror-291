from django.db import models

from .products_model import Products


class ComboSections(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(
        Products,
        db_table="combo-sections_products",
        blank=True,
        default=None,
    )

    class Meta:
        db_table = "combo_sections"


__all__ = ["ComboSections"]
