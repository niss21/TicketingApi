# Generated by Django 5.1.2 on 2024-10-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_vehicle_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='seat_number',
        ),
        migrations.AddField(
            model_name='seat',
            name='seat_id',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]