# Generated by Django 2.1.3 on 2019-04-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0006_remove_invoicetracker_po_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicetracker',
            name='po_reference',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]