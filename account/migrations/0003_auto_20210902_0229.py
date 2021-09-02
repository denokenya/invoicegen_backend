# Generated by Django 3.2.6 on 2021-09-01 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210821_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='createdBy',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='createdOn',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='modifiedBy',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='modifiedOn',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]