# Generated by Django 2.1.3 on 2018-12-18 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliercontactperson',
            name='email1',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='suppliercontactperson',
            name='email2',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='supplierprofile',
            name='office_email1',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='supplierprofile',
            name='office_email2',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
