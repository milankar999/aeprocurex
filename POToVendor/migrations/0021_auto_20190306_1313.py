# Generated by Django 2.1.3 on 2019-03-06 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POToVendor', '0020_auto_20190305_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpo',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Supplier.SupplierProfile'),
        ),
    ]
