# Generated by Django 3.2.6 on 2021-09-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0009_purchaseorderproduct_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='paymentTerms',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='tandc',
            field=models.TextField(default='', max_length=5000),
        ),
    ]