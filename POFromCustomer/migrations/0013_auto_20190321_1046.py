# Generated by Django 2.1.3 on 2019-03-21 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POFromCustomer', '0012_auto_20190320_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpolineitem',
            name='total_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='customerpo',
            name='total_basic_value',
            field=models.FloatField(default=0),
        ),
    ]
