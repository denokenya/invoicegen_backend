# Generated by Django 3.1.5 on 2021-08-05 10:55

import account.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_auto_20210802_1524"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companysetting",
            name="createdOn",
            field=models.DateTimeField(
                blank=True, default=account.models.today, null=True
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="createdOn",
            field=models.DateTimeField(
                blank=True, default=account.models.today, null=True
            ),
        ),
        migrations.AlterField(
            model_name="emailtemplate",
            name="createdOn",
            field=models.DateTimeField(
                blank=True, default=account.models.today, null=True
            ),
        ),
        migrations.AlterField(
            model_name="termandcondition",
            name="createdOn",
            field=models.DateTimeField(
                blank=True, default=account.models.today, null=True
            ),
        ),
        migrations.AlterField(
            model_name="usernote",
            name="createdOn",
            field=models.DateTimeField(
                blank=True, default=account.models.today, null=True
            ),
        ),
    ]
