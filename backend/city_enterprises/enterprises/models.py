from django.db import models

from districts.models import CityDistrict


class EnterpriseNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Сеть предприятий'
        verbose_name_plural = 'Сети предприятий'
        ordering = ['name']

    def __str__(self):
        return self.name


class Enterprise(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    enterprise_network = models.ForeignKey(
        EnterpriseNetwork, on_delete=models.CASCADE,
        related_name='enterprises', verbose_name='Сеть'
    )
    districts = models.ManyToManyField(
        CityDistrict, related_name='enterprises'
    )

    class Meta:
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.enterprise_network}'
