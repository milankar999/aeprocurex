# Generated by Django 2.1.3 on 2019-03-30 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0002_auto_20190330_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicetracker',
            name='financial_year',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
