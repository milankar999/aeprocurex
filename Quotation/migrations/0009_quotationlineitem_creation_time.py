# Generated by Django 2.1.3 on 2019-03-20 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0008_quotationlineitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationlineitem',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]