# Generated by Django 2.1.3 on 2018-12-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0007_customerprofile_tax_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='billing_address',
            field=models.TextField(blank=True, default='Same', null=True),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='shipping_address',
            field=models.TextField(blank=True, default='Same', null=True),
        ),
    ]
