# Generated by Django 2.1.3 on 2019-07-01 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SupplierPayment', '0005_auto_20190701_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierpaymentinfo',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
