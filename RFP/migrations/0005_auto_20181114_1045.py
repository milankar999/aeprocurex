# Generated by Django 2.1.3 on 2018-11-14 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0004_auto_20181114_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfplineitem',
            name='customer_lead_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='gst',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='target_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
