from django.contrib.auth.models import User, Group, Permission
from django.db import models
import uuid
from api.models import *
from django.utils import timezone
from invoicegen_backend.utils import PublicMediaStorage


def today():
    return timezone.localtime(timezone.now())


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, blank=True)
    logo = models.FileField(null=True, blank=True, storage=PublicMediaStorage())
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    panNo = models.CharField(max_length=10, default="", blank=True)
    orgType = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} | {self.gstin}"


class Address(models.Model):
    code = models.CharField(max_length=20, blank=True, unique=True)
    addrsType = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    line1 = models.CharField(max_length=100, blank=True, null=True)
    line2 = models.CharField(max_length=100, blank=True, null=True)
    line3 = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50)
    stateCode = models.IntegerField(default=22, blank=True, null=True)
    city = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=10, blank=True, null=True)
    typeCode = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    panNo = models.CharField(default="", max_length=10, blank=True)
    createdBy = models.EmailField(blank=True)
    createdOn = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modifiedBy = models.EmailField(blank=True)
    modifiedOn = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.name


class CompanyAddress(models.Model):
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE
    )
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.address.state} | {self.address.city}"


class Plant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL
    )
    address = models.ForeignKey(
        CompanyAddress, null=True, blank=True, on_delete=models.SET_NULL
    )
    monthRevenue = models.FloatField(default=0.0)
    yearRevenue = models.FloatField(default=0.0)
    establishmentYear = models.IntegerField()
    createdOn = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.address.address.city}"


class EmployeeType(models.Model):
    plant = models.ForeignKey(Plant, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, blank=False, null=False)
    accessibleModules = models.TextField(max_length=500, blank=True, null=True)


class Employee(User):
    code = models.CharField(max_length=100, blank=False, null=False)
    mobile = models.CharField(max_length=13, blank=False, null=False)
    panNo = models.CharField(max_length=10, blank=True, null=True)
    adhaarNo = models.CharField(max_length=12, blank=False, null=False)
    empType = models.ForeignKey(
        EmployeeType, null=True, blank=True, on_delete=models.SET_NULL
    )
    department = models.ForeignKey(
        Group, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.first_name + " " + self.last_name


class EmployeeAddress(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Driver(models.Model):
    department = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True
    )
    dp = models.URLField(default="", max_length=1000, null=True, blank=True)
    name = models.CharField(default="", max_length=100, blank=True, null=True)
    dob = models.DateField(
        default="", auto_now=False, auto_now_add=False, null=True, blank=True
    )
    dlNo = models.CharField(
        default="", max_length=128, unique=True, blank=True, null=True
    )
    remark = models.TextField(default="", max_length=200, blank=True, null=True)
    createdBy = models.EmailField(blank=True)
    createdOn = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modifiedBy = models.EmailField(blank=True)
    modifiedOn = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class DriverAddress(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Vehicle(models.Model):
    plant = models.ForeignKey(Plant, null=True, blank=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    vehicleCompany = models.CharField(default="", max_length=100, blank=True, null=True)
    vehiclemodel = models.CharField(default="", max_length=100, blank=True, null=True)
    vehicleRegistrationNo = models.CharField(
        default="", max_length=100, blank=True, null=True
    )
    loadingCapacity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.number


class Vendor(models.Model):
    code = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)


class VendorAddress(models.Model):
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.SET_NULL)
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.SET_NULL
    )


class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customerId = models.CharField(max_length=30, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    panNo = models.CharField(max_length=10, default="")
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    createdBy = models.EmailField(blank=True)
    modifiedOn = models.DateTimeField(auto_now=True, blank=True)
    modifiedBy = models.EmailField(blank=True)


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class CompanyCustomer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Ids(models.Model):
    name = models.TextField(null=True, blank=True)
    prefix = models.TextField(default="COMP")
    current = models.TextField(null=True, blank=True)
    upnext = models.TextField(null=True, blank=True)
    count = models.IntegerField(default=0)
    sep = models.TextField(default="", null=True, blank=True)
    mask = models.TextField(
        default="{prefix}{year}{month}{count}", null=True, blank=True
    )
    modifiedOn = models.DateTimeField(auto_now=True)


class Tax(models.Model):
    code = models.CharField(max_length=10)
    fullname = models.CharField(max_length=50, blank=True)
    percent = models.FloatField(default=0.0)
    use = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)


class IdsMap(models.Model):
    name = models.CharField(null=True, blank=True, max_length=20, unique=True)
    ids = models.ForeignKey(Ids, on_delete=models.CASCADE)


class UserNote(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="CreatedBy",
        on_delete=models.CASCADE,
    )
    title = models.TextField(default="", blank=True, null=True, max_length=50)
    note = models.TextField(default="", blank=True, null=True, max_length=200)
    createdOn = models.DateTimeField(default=today, blank=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True, blank=True, null=True)


class CompanySetting(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    key = models.CharField(max_length=4096, null=True, blank=True)
    createdOn = models.DateTimeField(default=today, blank=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True, blank=True, null=True)


class EmailTemplate(models.Model):
    setting = models.ForeignKey(CompanySetting, null=True, on_delete=models.CASCADE)
    model = models.CharField(max_length=50, null=False, blank=False)
    template = models.TextField(default="", blank=True, null=True, max_length=2000)
    createdOn = models.DateTimeField(default=today, blank=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True, blank=True, null=True)


class TermAndCondition(models.Model):
    setting = models.ForeignKey(CompanySetting, null=True, on_delete=models.CASCADE)
    model = models.CharField(max_length=50, null=False, blank=False)
    tc = models.TextField(max_length=2000, default="", blank=True)
    createdOn = models.DateTimeField(default=today, blank=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True, blank=True, null=True)


class UserConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    config = models.TextField()
    createdOn = models.DateTimeField(default=today, blank=True, null=True)