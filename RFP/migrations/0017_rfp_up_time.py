# Generated by Django 2.1.3 on 2019-05-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0016_auto_20190423_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfp',
            name='up_time',
            field=models.FloatField(default=0),
        ),
    ]
