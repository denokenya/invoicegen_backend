# Generated by Django 3.1.5 on 2021-08-02 09:16

import api.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, unique=True)),
                ('addrsType', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('line1', models.CharField(blank=True, max_length=100, null=True)),
                ('line2', models.CharField(blank=True, max_length=100, null=True)),
                ('line3', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(max_length=50)),
                ('stateCode', models.IntegerField(blank=True, default=22, null=True)),
                ('city', models.CharField(max_length=50)),
                ('postalCode', models.CharField(blank=True, max_length=10, null=True)),
                ('typeCode', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=13)),
                ('fax', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('gstin', models.CharField(blank=True, max_length=15, null=True)),
                ('panNo', models.CharField(blank=True, default='', max_length=10)),
                ('createdBy', models.EmailField(blank=True, max_length=254)),
                ('createdOn', models.DateTimeField(auto_now_add=True, null=True)),
                ('modifiedBy', models.EmailField(blank=True, max_length=254)),
                ('modifiedOn', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo')),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=13)),
                ('gstin', models.CharField(blank=True, max_length=15, null=True)),
                ('panNo', models.CharField(blank=True, default='', max_length=10)),
                ('orgType', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.address')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.company')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customerId', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=13)),
                ('gstin', models.CharField(blank=True, max_length=15, null=True)),
                ('panNo', models.CharField(default='', max_length=10)),
                ('createdOn', models.DateTimeField(blank=True, default=api.models.today, null=True)),
                ('createdBy', models.EmailField(blank=True, max_length=254)),
                ('modifiedOn', models.DateTimeField(auto_now=True)),
                ('modifiedBy', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('total', models.IntegerField()),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('code', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=13)),
                ('panNo', models.CharField(blank=True, max_length=10, null=True)),
                ('adhaarNo', models.CharField(max_length=12)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.department')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('prefix', models.TextField(default='COMP')),
                ('current', models.TextField(blank=True, null=True)),
                ('upnext', models.TextField(blank=True, null=True)),
                ('count', models.IntegerField(default=0)),
                ('sep', models.TextField(blank=True, default='', null=True)),
                ('mask', models.TextField(blank=True, default='{prefix}{year}{month}{count}', null=True)),
                ('modifiedOn', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('monthRevenue', models.FloatField(default=0.0)),
                ('yearRevenue', models.FloatField(default=0.0)),
                ('establishmentYear', models.IntegerField()),
                ('createdOn', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.companyaddress')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.company')),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('fullname', models.CharField(blank=True, max_length=50)),
                ('percent', models.FloatField(default=0.0)),
                ('use', models.BooleanField(default=False)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('updatedOn', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('employee_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='account.employee')),
                ('dlNo', models.CharField(blank=True, default='', max_length=128, null=True, unique=True)),
                ('remark', models.TextField(blank=True, default='', max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('account.employee',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VendorAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.address')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, unique=True)),
                ('vehicleCompany', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('vehiclemodel', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('vehicleRegistrationNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('loadingCapacity', models.FloatField(blank=True, null=True)),
                ('plant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.plant')),
            ],
        ),
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, default='', max_length=50, null=True)),
                ('note', models.TextField(blank=True, default='', max_length=200, null=True)),
                ('createdOn', models.DateTimeField(blank=True, default=api.models.today, null=True)),
                ('updatedOn', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='CreatedBy')),
            ],
        ),
        migrations.CreateModel(
            name='TermAndCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('tc', models.TextField(blank=True, default='', max_length=2000)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
            ],
        ),
        migrations.CreateModel(
            name='IdsMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('ids', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.ids')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('accessibleModules', models.TextField(blank=True, max_length=500, null=True)),
                ('plant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.plant')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.address')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='empType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.employeetype'),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('template', models.TextField(blank=True, default='', max_length=2000, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='plant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.plant'),
        ),
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
        ),
        migrations.CreateModel(
            name='CompanySetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=4096, null=True)),
                ('createdOn', models.DateTimeField(blank=True, default=api.models.today, null=True)),
                ('updatedOn', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.customer')),
            ],
        ),
    ]
