# Generated by Django 2.1.3 on 2018-12-10 04:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Sourcing', '0003_sourcinglineitem_mark'),
        ('Quotation', '0007_quotationtracker_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuotationLineitem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('product_code', models.CharField(blank=True, max_length=200, null=True)),
                ('part_number', models.CharField(blank=True, max_length=200, null=True)),
                ('pack_size', models.CharField(blank=True, max_length=200, null=True)),
                ('moq', models.CharField(blank=True, max_length=200, null=True)),
                ('hsn_code', models.CharField(blank=True, max_length=200, null=True)),
                ('gst', models.FloatField(blank=True, null=True)),
                ('quantity', models.FloatField()),
                ('uom', models.CharField(max_length=20)),
                ('unit_price', models.FloatField(blank=True, null=True)),
                ('margin', models.FloatField(blank=True, null=True)),
                ('lead_time', models.CharField(blank=True, max_length=200, null=True)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Quotation.QuotationTracker')),
                ('sourcing_lineitem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sourcing.SourcingLineitem')),
            ],
        ),
    ]
