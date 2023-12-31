# Generated by Django 4.2.3 on 2023-07-29 16:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('enterprises', '0001_initial'),
    ]

    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=100, null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='categories.category', verbose_name='Категория')),
                ('enterprise_network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='enterprises.enterprisenetwork', verbose_name='Сеть')),
            ],
            options={
                'verbose_name': 'Товар/Услуга',
                'verbose_name_plural': 'Товары/Услуги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_prices', to='enterprises.enterprise', verbose_name='Предприятие')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_prices', to='products.product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='enterprises',
            field=models.ManyToManyField(related_name='products', through='products.ProductPrice', to='enterprises.enterprise'),
        ),
        migrations.AddConstraint(
            model_name='productprice',
            constraint=models.UniqueConstraint(fields=('product', 'enterprise'), name='unique_enterprise_product'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('name', 'category', 'enterprise_network'), name='unique_product'),
        ),
    ]
