# Generated by Django 4.2.16 on 2025-01-06 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amphure',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name_th', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name_th', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('geography_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tambon',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('zip_code', models.IntegerField()),
                ('name_th', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('amphure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tambons', to='core.amphure')),
            ],
        ),
        migrations.AddField(
            model_name='amphure',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amphures', to='core.province'),
        ),
    ]
