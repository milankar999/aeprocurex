# Generated by Django 2.1.3 on 2019-05-07 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0025_vendorpo_creation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorpo',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]