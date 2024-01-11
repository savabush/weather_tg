from django.db import models
from django.db.models import Index


class Coordinate(models.Model):
    latitude = models.DecimalField(verbose_name='Широта', max_digits=5, decimal_places=2)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=5, decimal_places=2)

    name = models.CharField(verbose_name="Наименование города", max_length=255, db_index=True)

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"
        indexes = [
            Index(fields=('name',))
        ]

    def __str__(self) -> str:
        return self.name
