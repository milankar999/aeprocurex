# Generated by Django 2.1.3 on 2019-02-08 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POFromCustomer', '0004_auto_20190208_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpolineitem',
            name='category',
        ),
        migrations.AddField(
            model_name='cpolineitem',
            name='pack_size',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
