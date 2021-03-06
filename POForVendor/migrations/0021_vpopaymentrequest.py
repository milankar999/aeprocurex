# Generated by Django 2.1.3 on 2019-04-23 11:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0020_vendorpotracker_pending_payment_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='VPOPaymentRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('note', models.CharField(max_length=200)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(default='requested', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('vpo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POForVendor.VendorPOTracker')),
            ],
        ),
    ]
