# Generated by Django 2.1.3 on 2019-01-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0011_auto_20181128_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfp',
            name='creation_type',
            field=models.CharField(default='DEP', max_length=200),
        ),
    ]