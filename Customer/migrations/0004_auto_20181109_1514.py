# Generated by Django 2.1.3 on 2018-11-09 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0003_auto_20181109_1057'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customerprofile',
            unique_together=set(),
        ),
    ]
