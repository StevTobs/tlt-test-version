# Generated by Django 4.2.16 on 2025-01-15 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_calcostac_addon_total_calcostac_costtotal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calcostac',
            name='roi',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]