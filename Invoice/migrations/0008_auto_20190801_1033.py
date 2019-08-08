# Generated by Django 2.1.3 on 2019-08-01 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POFromCustomer', '0027_customerpo_processing_type'),
        ('POForVendor', '0033_auto_20190622_0740'),
        ('GRNIR', '0008_grnlineitem_invoiced_quantity'),
        ('Invoice', '0007_invoicetracker_po_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicelineitem',
            name='customer_po_lineitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='POFromCustomer.CPOLineitem'),
        ),
        migrations.AddField(
            model_name='invoicelineitem',
            name='grn_lineitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='GRNIR.GRNLineitem'),
        ),
        migrations.AddField(
            model_name='invoicelineitem',
            name='supplier_po_lineitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='POForVendor.VendorPOLineitems'),
        ),
    ]
