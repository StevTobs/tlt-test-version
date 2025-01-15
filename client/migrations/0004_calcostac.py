# Generated by Django 5.1.4 on 2025-01-09 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_addon_datacostelecac_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalcostAc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at_cost', models.DateTimeField(auto_now_add=True)),
                ('payback_period', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]