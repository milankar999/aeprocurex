# Generated by Django 2.1.3 on 2019-09-21 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POFromCustomer', '0028_cpolineitem_processing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpolineitem',
            name='indirect_processing_quantity',
            field=models.FloatField(default=0),
        ),
    ]