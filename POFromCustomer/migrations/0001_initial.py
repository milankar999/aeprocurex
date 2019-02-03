# Generated by Django 2.1.3 on 2019-01-30 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Quotation', '0008_quotationlineitem'),
        ('Customer', '0011_deliverycontactperson'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CPOApprovalDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('approved_date', models.DateTimeField(auto_now_add=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CPOAssign',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('assign_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CPOCreationDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CPOLineitem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('product_code', models.CharField(blank=True, max_length=200, null=True)),
                ('part_no', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('hsn_code', models.CharField(blank=True, max_length=10, null=True)),
                ('gst', models.FloatField(blank=True, null=True)),
                ('uom', models.CharField(default='Pcs', max_length=20)),
                ('quantity', models.FloatField()),
                ('unit_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPO',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_po_no', models.CharField(max_length=200)),
                ('customer_po_date', models.DateField()),
                ('delivery_date', models.DateField()),
                ('billing_address', models.TextField()),
                ('shipping_address', models.TextField()),
                ('inco_terms', models.CharField(max_length=200)),
                ('payment_terms', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=100)),
                ('cpo_approval_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CPOApprovalDetail')),
                ('cpo_assign_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CPOAssign')),
                ('cpo_creation_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CPOCreationDetail')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.CustomerProfile')),
                ('customer_contact_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.CustomerContactPerson')),
                ('delivery_contact_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.DeliveryContactPerson')),
            ],
        ),
        migrations.AddField(
            model_name='cpolineitem',
            name='cpo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CustomerPO'),
        ),
        migrations.AddField(
            model_name='cpolineitem',
            name='quotation_lineitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Quotation.QuotationLineitem'),
        ),
    ]
