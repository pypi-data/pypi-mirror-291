from django.db import models


class Allergens(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "allergens"


__all__ = ["Allergens"]
