# Generated by Django 2.1.3 on 2019-09-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0010_profile_cpo_editing'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rfp_editing',
            field=models.CharField(default='no', max_length=50),
        ),
    ]
