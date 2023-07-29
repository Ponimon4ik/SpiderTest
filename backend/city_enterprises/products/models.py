from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator

from categories.models import Category
from enterprises.models import Enterprise, EnterpriseNetwork


NOT_MATCH_NETWORK = 'Предприятие должно принадлежать той же сети, что и продукт.'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products',
        verbose_name='Категория'
    )
    description = models.TextField(max_length=100, verbose_name='Описание', null=True, blank=True)
    enterprise_network = models.ForeignKey(
        EnterpriseNetwork, on_delete=models.CASCADE, related_name='products',
        verbose_name='Сеть'
    )
    enterprises = models.ManyToManyField(
        Enterprise, through='ProductPrice', related_name='products'
    )

    class Meta:
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category', 'enterprise_network'],
                name='unique_product'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.category.name}, {self.enterprise_network.name}'


class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='products_prices')
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, verbose_name='Предприятие',
        related_name='products_prices'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'enterprise'],
                name='unique_enterprise_product'
            )
        ]

    def __str__(self):
        return f'{self.product.name}, {self.enterprise.name}, {self.price}'

    def clean(self):
        super().clean()
        if self.product.enterprise_network != self.enterprise.enterprise_network:
            raise ValidationError(NOT_MATCH_NETWORK)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
