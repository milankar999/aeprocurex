# Generated by Django 2.1.3 on 2019-02-07 10:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0008_quotationlineitem'),
        ('POFromCustomer', '0002_auto_20190130_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPOSelectedQuotation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('CustomerPO', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POFromCustomer.CustomerPO')),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quotation.QuotationTracker')),
            ],
        ),
    ]
