# Generated by Django 2.1.3 on 2019-02-15 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POToVendor', '0006_auto_20190215_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpo',
            name='po_number',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
