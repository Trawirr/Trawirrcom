# Generated by Django 4.1 on 2022-09-19 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civilization', '0005_remove_tile_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='height',
            field=models.FloatField(),
        ),
    ]
