# Generated by Django 2.1.3 on 2018-11-05 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('mobileNo1', models.CharField(blank=True, max_length=20, null=True)),
                ('mobileNo2', models.CharField(blank=True, max_length=20, null=True)),
                ('email1', models.EmailField(blank=True, max_length=50, null=True)),
                ('email2', models.EmailField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('pin', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('office_email1', models.EmailField(blank=True, max_length=20, null=True)),
                ('office_email2', models.EmailField(blank=True, max_length=20, null=True)),
                ('office_phone1', models.CharField(blank=True, max_length=20, null=True)),
                ('office_phone2', models.CharField(blank=True, max_length=20, null=True)),
                ('gst_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('vendor_code', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_term', models.IntegerField(blank=True, null=True)),
                ('inco_term', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EndUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('department_name', models.CharField(max_length=200)),
                ('mobileNo1', models.CharField(blank=True, max_length=20, null=True)),
                ('mobileNo2', models.CharField(blank=True, max_length=20, null=True)),
                ('email1', models.EmailField(blank=True, max_length=20, null=True)),
                ('email2', models.EmailField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.CustomerProfile')),
            ],
        ),
        migrations.AddField(
            model_name='customercontactperson',
            name='customer_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.CustomerProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='customerprofile',
            unique_together={('name', 'location')},
        ),
    ]
