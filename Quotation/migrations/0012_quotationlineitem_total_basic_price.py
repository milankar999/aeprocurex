# Generated by Django 2.1.3 on 2019-03-26 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0011_auto_20190326_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationlineitem',
            name='total_basic_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]