# Generated by Django 3.2.6 on 2021-09-06 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='createdBy',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='createdOn',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='dlNo',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='dp',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='modifiedBy',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='modifiedOn',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='name',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='remark',
        ),
    ]