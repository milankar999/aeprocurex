# Generated by Django 2.1.3 on 2019-02-13 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('POToVendor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vpolineitems',
            name='cpo_lineitem',
        ),
        migrations.DeleteModel(
            name='VPOLineitems',
        ),
    ]
