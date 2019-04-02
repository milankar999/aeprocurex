# Generated by Django 2.1.3 on 2019-03-23 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('POFromCustomer', '0016_customerpo_total_value'),
        ('Supplier', '0002_auto_20181218_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPO',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('offer_reference', models.CharField(blank=True, max_length=100, null=True)),
                ('offer_date', models.DateField(blank=True, null=True)),
                ('billing_address', models.TextField(blank=True, null=True)),
                ('shipping_address', models.TextField(blank=True, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=200, null=True)),
                ('receiver_phone1', models.CharField(blank=True, max_length=20, null=True)),
                ('receiver_phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('receiver_dept', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_term', models.IntegerField(default=0)),
                ('advance_percentage', models.IntegerField(default=0)),
                ('freight_charges', models.FloatField(default=0.0)),
                ('custom_duties', models.FloatField(default=0.0)),
                ('pf', models.FloatField(default=0.0)),
                ('insurance', models.FloatField(default=0.0)),
                ('mode_of_transport', models.CharField(blank=True, max_length=200, null=True)),
                ('inco_terms', models.CharField(blank=True, max_length=200, null=True)),
                ('installation', models.CharField(blank=True, max_length=200, null=True)),
                ('terms_of_payment', models.CharField(blank=True, max_length=200, null=True)),
                ('currency', models.CharField(default='INR', max_length=20)),
                ('comments', models.TextField(blank=True, null=True)),
                ('po_status', models.CharField(default='Preparing', max_length=50)),
                ('di1', models.TextField(default='1.Original Invoice & Delivery Challans Four (4) copies each must be submitted at the time of delivery of goods')),
                ('di2', models.TextField(default='2.Entire Goods must be delivered in Single Lot if not specified otherwise. For any changes, must inform IMMEDIATELY.')),
                ('di3', models.TextField(default='3.Product Specifications, Qty, Price, Delivery Terms are in accordance with your offer')),
                ('di4', models.TextField(default='4.Product Specifications, Qty, Price, Delivery Terms shall remain unchanged for this order.')),
                ('di5', models.TextField(default='5.Notify any delay in shipment as scheduled IMMEDIATELY.')),
                ('di6', models.TextField(default='6.Mail all correspondance to corporate office address only.')),
                ('di7', models.TextField(default='7.Must Submit Warranty Certificate, PO copy, TC copy (if any) and all other documents as per standard documentation')),
                ('di8', models.TextField(blank=True, null=True)),
                ('di9', models.TextField(blank=True, null=True)),
                ('di10', models.TextField(blank=True, null=True)),
                ('cpo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CustomerPO')),
                ('requester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Supplier.SupplierProfile')),
                ('vendor_contact_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Supplier.SupplierContactPerson')),
            ],
        ),
        migrations.CreateModel(
            name='VendorPOLineitems',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('product_code', models.CharField(blank=True, max_length=200, null=True)),
                ('hsn_code', models.CharField(blank=True, max_length=10, null=True)),
                ('pack_size', models.CharField(blank=True, max_length=10, null=True)),
                ('gst', models.FloatField(blank=True, null=True)),
                ('uom', models.CharField(default='Pcs', max_length=20)),
                ('quantity', models.FloatField()),
                ('unit_price', models.FloatField()),
                ('discount', models.FloatField(blank=True, default=0, null=True)),
                ('cpo_lineitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CPOLineitem')),
                ('vpo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vpo_lineitems', to='POForVendor.VendorPO')),
            ],
        ),
        migrations.CreateModel(
            name='VendorPOTracker',
            fields=[
                ('po_number', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('po_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default='Requested', max_length=50)),
                ('requester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vpo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POForVendor.VendorPO')),
            ],
        ),
    ]