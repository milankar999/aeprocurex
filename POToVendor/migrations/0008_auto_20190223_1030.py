# Generated by Django 2.1.3 on 2019-02-23 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('POToVendor', '0007_auto_20190215_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpo',
            name='insurance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='vpo',
            name='po_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vpolineitems',
            name='vpo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vpo_lineitems', to='POToVendor.VPO'),
        ),
    ]