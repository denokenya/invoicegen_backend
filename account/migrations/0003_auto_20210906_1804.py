# Generated by Django 3.2.6 on 2021-09-06 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210906_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driveraddress',
            name='address',
        ),
        migrations.RemoveField(
            model_name='driveraddress',
            name='driver',
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
        migrations.DeleteModel(
            name='DriverAddress',
        ),
    ]