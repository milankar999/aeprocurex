# Generated by Django 2.1.3 on 2019-04-20 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0015_auto_20190420_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorpo',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='POForVendor.CurrencyIndex'),
        ),
    ]
