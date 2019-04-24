# Generated by Django 2.1.3 on 2019-04-23 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RFP', '0015_rfplineitem_creation_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='RFPStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=200)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='rfp',
            name='current_sourcing_status',
            field=models.CharField(default='Not Mentioned', max_length=200),
        ),
        migrations.AddField(
            model_name='rfpstatus',
            name='rfp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RFP.RFP'),
        ),
        migrations.AddField(
            model_name='rfpstatus',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
