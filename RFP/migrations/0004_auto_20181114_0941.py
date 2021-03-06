# Generated by Django 2.1.3 on 2018-11-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0003_auto_20181112_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfplineitem',
            name='uom',
            field=models.CharField(default='Pcs', max_length=20),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='brand',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='category',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='customer_lead_time',
            field=models.FloatField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='gst',
            field=models.FloatField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='hsn_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='model',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='part_no',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='product_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='remarks',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='rfplineitem',
            name='target_price',
            field=models.FloatField(blank=True, max_length=200, null=True),
        ),
    ]
