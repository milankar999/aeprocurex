# Generated by Django 2.1.3 on 2019-09-19 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0019_auto_20190916_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfp',
            name='merge_status',
            field=models.BooleanField(default=False),
        ),
    ]