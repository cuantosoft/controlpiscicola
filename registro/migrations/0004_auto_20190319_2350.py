# Generated by Django 2.1.5 on 2019-03-20 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0003_auto_20190302_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estanque',
            name='mts_2',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]