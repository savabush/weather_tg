# Generated by Django 5.0.1 on 2024-01-11 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coordinate',
            options={'verbose_name': 'Координаты'},
        ),
    ]