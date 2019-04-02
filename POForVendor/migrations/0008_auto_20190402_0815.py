# Generated by Django 2.1.3 on 2019-04-02 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0007_auto_20190329_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorpo',
            name='billing_address',
            field=models.TextField(default='Aeprocurex Sourcing Private Limited, Shankarappa Complex #4, Hosapalya Main Road, Opposite to Om Shakti Temple, Hosapalya, HSR Layout Extension, Bangalore - 560068'),
        ),
        migrations.AlterField(
            model_name='vendorpo',
            name='inco_terms',
            field=models.CharField(default='DAP', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendorpo',
            name='installation',
            field=models.CharField(default='Supplier Scope', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendorpo',
            name='mode_of_transport',
            field=models.CharField(default='Road', max_length=200),
        ),
        migrations.AlterField(
            model_name='vendorpo',
            name='shipping_address',
            field=models.TextField(default='Aeprocurex Sourcing Private Limited No 1318, 3rd Floor, 24th Main Rd, Sector 2, HSR Layout, Bengaluru, Karnataka 560102'),
        ),
    ]
