# Generated by Django 2.1.3 on 2019-03-27 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0004_vendorpolineitems_actual_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorpotracker',
            name='all_total_value',
            field=models.FloatField(default=0),
        ),
    ]