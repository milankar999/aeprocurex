# Generated by Django 2.1.3 on 2018-11-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sourcing', '0002_sourcinglineitem_expected_freight'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcinglineitem',
            name='mark',
            field=models.CharField(default='False', max_length=10),
        ),
    ]
