# Generated by Django 5.1 on 2024-08-24 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0027_table_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='table',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.DeleteModel(
            name='Table',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
