# Generated by Django 2.1.3 on 2019-11-18 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0011_profile_rfp_editing'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='customer_editing',
            field=models.CharField(default='no', max_length=50),
        ),
    ]
