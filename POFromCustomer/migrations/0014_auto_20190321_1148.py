# Generated by Django 2.1.3 on 2019-03-21 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POFromCustomer', '0013_auto_20190321_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerpo',
            name='document1',
            field=models.FileField(blank=True, null=True, upload_to='cpo/'),
        ),
        migrations.AddField(
            model_name='customerpo',
            name='document2',
            field=models.FileField(blank=True, null=True, upload_to='cpo/'),
        ),
    ]
