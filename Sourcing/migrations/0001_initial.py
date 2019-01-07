# Generated by Django 2.1.3 on 2018-11-20 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('RFP', '0010_auto_20181117_1004'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sourcing',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('offer_reference', models.CharField(max_length=200)),
                ('offer_date', models.DateField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rfp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RFP.RFP')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Supplier.SupplierProfile')),
                ('supplier_contact_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Supplier.SupplierContactPerson')),
            ],
        ),
        migrations.CreateModel(
            name='SourcingLineitem',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('product_title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('model', models.CharField(blank=True, max_length=200, null=True)),
                ('brand', models.CharField(blank=True, max_length=200, null=True)),
                ('product_code', models.CharField(blank=True, max_length=200, null=True)),
                ('pack_size', models.CharField(blank=True, max_length=200, null=True)),
                ('moq', models.CharField(blank=True, max_length=200, null=True)),
                ('lead_time', models.CharField(blank=True, max_length=200, null=True)),
                ('price_validity', models.CharField(blank=True, max_length=200, null=True)),
                ('mrp', models.FloatField(blank=True, null=True)),
                ('price1', models.FloatField(blank=True, null=True)),
                ('price2', models.FloatField(blank=True, null=True)),
                ('rfp_lineitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RFP.RFPLineitem')),
                ('sourcing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sourcing.Sourcing')),
            ],
        ),
    ]
