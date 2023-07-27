# Generated by Django 4.2.3 on 2023-07-27 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('districts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnterpriseNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Сеть предприятий',
                'verbose_name_plural': 'Сети предприятий',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('districts', models.ManyToManyField(related_name='enterprises', to='districts.citydistrict')),
                ('enterprise_network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprises', to='enterprises.enterprisenetwork', verbose_name='Сеть')),
            ],
            options={
                'verbose_name': 'Предприятие',
                'verbose_name_plural': 'Предприятия',
                'ordering': ['name'],
            },
        ),
    ]
