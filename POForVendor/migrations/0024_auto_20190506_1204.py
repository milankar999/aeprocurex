# Generated by Django 2.1.3 on 2019-05-06 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0023_vendorpotracker_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorpo',
            name='cpo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CustomerPO'),
        ),
    ]
