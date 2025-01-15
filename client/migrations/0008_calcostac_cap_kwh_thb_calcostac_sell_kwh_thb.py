# Generated by Django 4.2.16 on 2025-01-15 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_calcostac_roi'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcostac',
            name='cap_kwh_thb',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='calcostac',
            name='sell_kwh_thb',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
