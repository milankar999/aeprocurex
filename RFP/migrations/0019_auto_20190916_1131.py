# Generated by Django 2.1.3 on 2019-09-16 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0018_auto_20190808_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfp',
            name='freight_charges',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rfp',
            name='pf_charges',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
