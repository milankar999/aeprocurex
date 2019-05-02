# Generated by Django 2.1.3 on 2019-05-02 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SupplierPayment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplierpaymentinfo',
            name='attachment2',
        ),
        migrations.RemoveField(
            model_name='supplierpaymentinfo',
            name='attachment3',
        ),
        migrations.RemoveField(
            model_name='supplierpaymentrequest',
            name='attachment2',
        ),
        migrations.RemoveField(
            model_name='supplierpaymentrequest',
            name='attachment3',
        ),
        migrations.AddField(
            model_name='supplierpaymentinfo',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]