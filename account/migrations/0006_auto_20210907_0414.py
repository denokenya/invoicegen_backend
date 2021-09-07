# Generated by Django 3.2.6 on 2021-09-06 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_tax_usearea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendoraddress',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.address'),
        ),
        migrations.AlterField(
            model_name='vendoraddress',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.vendor'),
        ),
    ]
