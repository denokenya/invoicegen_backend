# Generated by Django 3.2.6 on 2021-09-07 08:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_purchaseorder_costcenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='poTotalAmount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='poTotalAmountWithTax',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToAddrsLine1',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToAddrsLine2',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToAddrsLine3',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToCity',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToEmail',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToGSTIN',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToName',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToPanNo',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToPhone',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToPostalCode',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='shipToState',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='poNumber',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
