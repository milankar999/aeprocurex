# Generated by Django 2.1.3 on 2019-03-20 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFP', '0014_auto_20190314_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfplineitem',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]