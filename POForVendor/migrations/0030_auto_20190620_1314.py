# Generated by Django 2.1.3 on 2019-06-20 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0029_paymentterms_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentterms',
            name='id',
        ),
        migrations.AlterField(
            model_name='paymentterms',
            name='text',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
