# Generated by Django 2.1.3 on 2019-05-22 06:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0026_vendorpo_creation_time'),
        ('GRNIR', '0004_auto_20190517_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='IRAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('document_no', models.CharField(blank=True, max_length=100, null=True)),
                ('document_date', models.DateField()),
                ('attachment', models.FileField(upload_to='ir_document/')),
            ],
        ),
        migrations.CreateModel(
            name='IRTracker',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_no', models.CharField(max_length=200)),
                ('invoice_date', models.DateTimeField()),
                ('total_basic_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('inr_value', models.FloatField(default=1)),
                ('converted_total_basic_price', models.FloatField()),
                ('converted_total_price', models.FloatField()),
                ('grn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GRNIR.GRNTracker')),
                ('received_currency', models.ForeignKey(default='Indian Rupees', on_delete=django.db.models.deletion.CASCADE, to='POForVendor.CurrencyIndex')),
            ],
        ),
        migrations.AddField(
            model_name='irattachment',
            name='ir',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GRNIR.IRTracker'),
        ),
    ]
