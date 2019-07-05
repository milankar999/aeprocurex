# Generated by Django 2.1.3 on 2019-07-02 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SupplierPayment', '0006_auto_20190701_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierpaymentinfo',
            name='transaction_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='supplierpaymentinfo',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
