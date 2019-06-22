# Generated by Django 2.1.3 on 2019-06-20 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('POForVendor', '0031_auto_20190620_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTerms',
            fields=[
                ('text', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('days', models.IntegerField(default=0)),
                ('advance_percentage', models.IntegerField(default=100)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='vendorpo',
            name='payment_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='POForVendor.PaymentTerms'),
        ),
    ]