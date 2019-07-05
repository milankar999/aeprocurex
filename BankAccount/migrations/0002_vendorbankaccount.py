# Generated by Django 2.1.3 on 2019-06-28 12:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Supplier', '0002_auto_20181218_1856'),
        ('BankAccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorBankAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=200)),
                ('branch', models.CharField(blank=True, max_length=200, null=True)),
                ('account_holder', models.CharField(max_length=200)),
                ('ifcs_code', models.CharField(max_length=200)),
                ('account_type', models.CharField(max_length=200)),
                ('acknowledgement', models.CharField(default='no', max_length=200)),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Supplier.SupplierProfile')),
            ],
        ),
    ]
