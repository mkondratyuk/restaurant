# Generated by Django 5.0.1 on 2024-07-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0015_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(to='restaurant.dish'),
        ),
    ]
