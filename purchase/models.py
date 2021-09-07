from django.db import models
from api.models import *
import uuid
# Create your models here.

class PurchaseOrder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    poNumber = models.CharField(null=False, blank=False, max_length=100, unique=True)
    # company
    orgName = models.CharField(max_length=100, blank=True)
    orgAddrsLine1 = models.TextField(max_length=200, blank=True)
    orgAddrsLine2 = models.TextField(max_length=200, blank=True)
    orgAddrsLine3 = models.TextField(max_length=200, blank=True)
    orgEmail = models.EmailField(null=True, blank=True)
    orgPhone = models.CharField(max_length=13, blank=True)
    orgFax = models.CharField(max_length=20, blank=True)
    orgState = models.CharField(max_length=50, blank=True)
    orgCity = models.CharField(max_length=50, blank=True)
    orgPostalCode = models.CharField(max_length=8, blank=True)
    orgGSTIN = models.CharField(max_length=15, blank=True)
    orgLogo = models.URLField(null=True, blank=True)
    orgPanNo = models.CharField(max_length=10, default="")
    
    # vendor
    vendorName = models.CharField(max_length=50, blank=True)
    vendorAddrsLine1 = models.CharField(max_length=50, blank=True)
    vendorAddrsLine2 = models.CharField(max_length=50, blank=True)
    vendorAddrsLine3 = models.CharField(max_length=50, blank=True)
    vendorState = models.CharField(max_length=50, blank=True)
    vendorCity = models.CharField(max_length=50, blank=True)
    vendorPostalCode = models.CharField(max_length=8, blank=True)
    vendorPhone = models.CharField(max_length=50, blank=True)
    vendorEmail = models.CharField(max_length=50, blank=True)
    vendorPanNo = models.CharField(max_length=50, blank=True)
    vendorGSTIN = models.CharField(max_length=50, blank=True)
    
    # shipping
    shipToName = models.CharField(max_length=50, blank=True)
    shipToAddrsLine1 = models.CharField(max_length=50, blank=True)
    shipToAddrsLine2 = models.CharField(max_length=50, blank=True)
    shipToAddrsLine3 = models.CharField(max_length=50, blank=True)
    shipToState = models.CharField(max_length=50, blank=True)
    shipToCity = models.CharField(max_length=50, blank=True)
    shipToPostalCode = models.CharField(max_length=8, blank=True)
    shipToPhone = models.CharField(max_length=50, blank=True)
    shipToEmail = models.CharField(max_length=50, blank=True)
    shipToPanNo = models.CharField(max_length=50, blank=True)
    shipToGSTIN = models.CharField(max_length=50, blank=True)
    
    poTotalAmount = models.FloatField()
    poTotalAmountWithTax = models.FloatField()
    
    costcenter = models.CharField(default="", max_length=100, blank=True, null=True)
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    createdBy = models.EmailField(blank=True)
    
    def __str__(self):
        return f'{self.poNumber}'


class PurchaseOrderProduct(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    code = models.CharField(default="", max_length=50)
    name = models.CharField(default="", max_length=50)
    uom = models.CharField(default="", max_length=50)
    qty = models.FloatField()

class PurchaseOrderTax(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    taxName = models.CharField(default="", max_length=100)
    taxPercent = models.FloatField()