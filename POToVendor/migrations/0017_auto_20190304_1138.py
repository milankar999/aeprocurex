# Generated by Django 2.1.3 on 2019-03-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POToVendor', '0016_vpotracker_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vpo',
            name='discount',
        ),
        migrations.AddField(
            model_name='vpolineitems',
            name='discount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
