# Generated by Django 3.2.6 on 2021-09-01 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210902_0229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='vehicleRegistrationNo',
        ),
    ]
