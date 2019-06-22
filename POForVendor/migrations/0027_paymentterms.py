# Generated by Django 2.1.3 on 2019-06-06 06:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('POForVendor', '0026_vendorpo_creation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTerms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('days', models.IntegerField(default=0)),
                ('advance_percentage', models.IntegerField(default=100)),
            ],
        ),
    ]
