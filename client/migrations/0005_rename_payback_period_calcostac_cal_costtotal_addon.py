# Generated by Django 5.1.4 on 2025-01-09 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_calcostac'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calcostac',
            old_name='payback_period',
            new_name='cal_costtotal_addon',
        ),
    ]