# Generated by Django 5.0.1 on 2024-07-06 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_myrating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='myrating',
            unique_together=set(),
        ),
    ]
