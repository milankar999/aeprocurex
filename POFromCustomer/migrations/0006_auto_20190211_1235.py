# Generated by Django 2.1.3 on 2019-02-11 07:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('POFromCustomer', '0005_auto_20190208_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpoassign',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]