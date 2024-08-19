from django.db import models


class ComboIngredients(models.Model):
    name = models.CharField(max_length=255)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "combo_ingredients"


__all__ = ["ComboIngredients"]
