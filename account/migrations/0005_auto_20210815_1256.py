# Generated by Django 3.1.5 on 2021-08-15 07:26

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('account', '0004_userconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfig',
            name='createdOn',
            field=models.DateTimeField(blank=True, default=account.models.today, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
    ]
