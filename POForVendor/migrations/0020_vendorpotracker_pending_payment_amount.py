# Generated by Django 2.1.3 on 2019-04-23 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0019_vendorpotracker_non_inr_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorpotracker',
            name='pending_payment_amount',
            field=models.FloatField(default=0),
        ),
    ]