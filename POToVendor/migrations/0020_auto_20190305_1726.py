# Generated by Django 2.1.3 on 2019-03-05 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POToVendor', '0019_auto_20190305_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpo',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_profile', to='Supplier.SupplierProfile'),
        ),
    ]