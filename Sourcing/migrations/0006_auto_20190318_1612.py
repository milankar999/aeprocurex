# Generated by Django 2.1.3 on 2019-03-18 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sourcing', '0005_auto_20190315_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfq',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
