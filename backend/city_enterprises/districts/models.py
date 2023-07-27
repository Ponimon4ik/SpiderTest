from django.db import models


class CityDistrict(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Район города'
        verbose_name_plural = 'Районы города'
        ordering = ['name']

    def __str__(self):
        return self.name
