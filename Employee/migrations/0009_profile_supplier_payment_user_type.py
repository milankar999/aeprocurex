# Generated by Django 2.1.3 on 2019-04-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0008_auto_20190227_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='supplier_payment_user_type',
            field=models.CharField(default='user', max_length=50),
        ),
    ]
