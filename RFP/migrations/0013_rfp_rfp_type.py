# Generated by Django 2.1.3 on 2019-01-22 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0012_rfp_creation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfp',
            name='rfp_type',
            field=models.CharField(default='Regular', max_length=200),
        ),
    ]
