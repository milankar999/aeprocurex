# Generated by Django 2.1.3 on 2018-11-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0010_auto_20181117_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfp',
            name='single_vendor_approval',
            field=models.CharField(default='No', max_length=10),
        ),
        migrations.AddField(
            model_name='rfp',
            name='single_vendor_reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]
