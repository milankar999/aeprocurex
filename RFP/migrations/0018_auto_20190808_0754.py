# Generated by Django 2.1.3 on 2019-08-08 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0017_rfp_up_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfplineitem',
            name='target_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]