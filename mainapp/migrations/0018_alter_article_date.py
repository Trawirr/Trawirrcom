# Generated by Django 4.1 on 2022-09-19 21:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_alter_article_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 19, 23, 22, 21, 918172)),
        ),
    ]
