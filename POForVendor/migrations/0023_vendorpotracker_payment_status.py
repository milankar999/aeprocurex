# Generated by Django 2.1.3 on 2019-04-27 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0022_auto_20190426_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorpotracker',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]