from django.dispatch import receiver
from django.db import models
from account.models import Plant
from invoicegen_backend import settings
import uuid
from api.models import *
from django.db.models.signals import post_save, post_delete


class RawMaterial(models.Model):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    uom = models.CharField(max_length=20, default="MT")
    createdOn = models.DateTimeField(default=today, null=True, blank=True)


class Stock(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    plant = models.ForeignKey(Plant, null=True, blank=True, on_delete=models.CASCADE)
    material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    current = models.IntegerField()
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    modifiedOn = models.DateTimeField(auto_now=True, blank=True)


class StockEntry(models.Model):
    materialName = models.CharField(max_length=200, null=False, blank=False)
    materialCode = models.CharField(max_length=128, null=False, blank=False)
    materialUom = models.CharField(max_length=20, null=False, blank=False)
    materialQty = models.FloatField(null=False, blank=False)
    challanNo = models.CharField(max_length=128, null=False, blank=False)
    challanDate = models.CharField(max_length=128, null=False, blank=False)
    purchaseOrder = models.CharField(max_length=128, null=False, blank=False)
    vehicleNo = models.CharField(max_length=50, null=False, blank=False)
    driverName = models.CharField(max_length=200, null=False, blank=False)
    driverCode = models.CharField(max_length=128, null=False, blank=False)
    moisture = models.FloatField(null=False, blank=False)
    remark = models.TextField(default="", max_length=500, null=True, blank=True)
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    createdBy = models.CharField(default="", max_length=100)


def onAddedStockMaterial(stockentry):
    matCode = stockentry.materialCode
    matQty = stockentry.materialQty
    stock = Stock.objects.filter(material__code=matCode)[0]
    stock.current = stock.current+matQty
    stock.save()

def onDeletedStockMaterial(stockentry):
    matCode = stockentry.materialCode
    matQty = stockentry.materialQty
    stock = Stock.objects.filter(material__code=matCode)[0]
    stock.current = stock.current-matQty
    stock.save()

@receiver(post_save, sender=StockEntry)
def post_save_stockentry(sender, instance, created, *args, **kwargs):
    if created:
        try:
            onAddedStockMaterial(instance)
        except:
            pass
@receiver(post_delete, sender=StockEntry)
def post_delete_stockentry(sender, instance, created, *args, **kwargs):
    if created:
        try:
            onDeletedStockMaterial(instance)
        except:
            pass

