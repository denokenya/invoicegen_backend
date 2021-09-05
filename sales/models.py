from django.db import models
from account.models import Customer, Plant
from api.models import *
import uuid

# SALE ORDER
class SaleOrder(models.Model):
    # id and number
    saleOrderId = models.CharField(max_length=30, unique=True)
    poNumber = models.CharField(max_length=50, blank=True)
    poDate = models.DateField(null=True, blank=True)
    customerId = models.CharField(max_length=50, blank=True)

    # comapny
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

    # billing
    billToName = models.CharField(max_length=50, blank=True)
    billToAddrsLine1 = models.CharField(max_length=50, blank=True)
    billToAddrsLine2 = models.CharField(max_length=50, blank=True)
    billToAddrsLine3 = models.CharField(max_length=50, blank=True)
    billToState = models.CharField(max_length=50, blank=True)
    billToCity = models.CharField(max_length=50, blank=True)
    billToPostalCode = models.CharField(max_length=8, blank=True)
    billToPhone = models.CharField(max_length=50, blank=True)
    billToEmail = models.CharField(max_length=50, blank=True)
    billToPanNo = models.CharField(max_length=50, blank=True)
    billToGSTIN = models.CharField(max_length=50, blank=True)
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

    siteDistance = models.FloatField(default=0.0, null=True, blank=True)
    paymentTerms = models.TextField(default="", max_length=1000)
    totalAmount = models.FloatField(default=0.0)
    expired = models.BooleanField(default=False)
    status = models.CharField(default="OPEN", max_length=10)
    dueDate = models.DateField(auto_now=True)
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    completedOn = models.DateField(null=True, blank=True)
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    createdBy = models.EmailField(blank=True)
    
    def __str__(self):
        return self.saleOrderId
    


class SaleOrderProductLine(models.Model):
    saleOrder = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    sopCode = models.CharField(max_length=20, blank=True)
    sopName = models.CharField(max_length=50)
    sopDescription = models.CharField(max_length=50, blank=True)
    sopHsnCode = models.CharField(max_length=20, blank=True)
    sopUom = models.CharField(max_length=5)
    sopRate = models.FloatField(max_length=0.0)
    sopQty = models.FloatField(default=0.0)
    sopDeliveredQty = models.FloatField(default=0.0)


class SaleOrderTax(models.Model):
    saleOrder = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    taxName = models.CharField(max_length=20, blank=True)
    taxPercent = models.FloatField(default=0.0, blank=True)


class PlantSaleOrder(models.Model):
    plant = models.ForeignKey(Plant, null=True, on_delete=models.SET_NULL)
    saleOrder = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)


class Invoice(models.Model):
    invoiceId = models.CharField(max_length=30, unique=True)
    soNumber = models.CharField(max_length=50, blank=True)
    poNumber = models.CharField(max_length=50, blank=True)
    deliveryDate = models.DateField(blank=True, null=True)
    customerId = models.CharField(max_length=20, blank=True)

    # comapny
    orgName = models.CharField(max_length=100, blank=True)
    orgAddrsLine1 = models.TextField(max_length=200, blank=True)
    orgAddrsLine2 = models.TextField(max_length=200, blank=True)
    orgAddrsLine3 = models.TextField(max_length=200, blank=True)
    orgEmail = models.EmailField(null=True, blank=True)
    orgPhone = models.CharField(max_length=13, blank=True)
    orgFax = models.CharField(max_length=20, blank=True)
    orgCity = models.CharField(max_length=50, blank=True)
    orgPostalCode = models.CharField(max_length=10, blank=True)
    orgState = models.CharField(max_length=50, blank=True)
    orgGSTIN = models.CharField(max_length=15, blank=True)
    orgLogo = models.URLField(null=True, blank=True)
    orgPanNo = models.CharField(max_length=10, default="")

    # billing
    billToName = models.CharField(max_length=50, blank=True)
    billToAddrsLine1 = models.CharField(max_length=50, blank=True)
    billToAddrsLine2 = models.CharField(max_length=50, blank=True)
    billToAddrsLine3 = models.CharField(max_length=50, blank=True)
    billToState = models.CharField(max_length=50, blank=True)
    billToCity = models.CharField(max_length=50, blank=True)
    billToPostalCode = models.CharField(max_length=8, blank=True)
    billToPhone = models.CharField(max_length=50, blank=True)
    billToEmail = models.CharField(max_length=50, blank=True)
    billToPanNo = models.CharField(max_length=50, blank=True)
    billToGSTIN = models.CharField(max_length=50, blank=True)
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

    transportMode = models.CharField(default="Road", max_length=20)
    transporterCode = models.CharField(default="", max_length=20, blank=True)
    transporterName = models.CharField(default="", max_length=50, blank=True)
    vehicleRegNo = models.CharField(default="", max_length=50)
    lrOrRrNo = models.CharField(default="", max_length=50, blank=True)
    lrOrRrDate = models.DateField(null=True, blank=True)
    ewayBillNo = models.CharField(default="", max_length=50, blank=True)
    ewayBillDatetime = models.DateTimeField(blank=True, null=True)
    placeOfSupply = models.CharField(default="Raipur", max_length=50)
    perticulars = models.TextField(default="", max_length=200, blank=True)
    paymentTerms = models.TextField(default="", max_length=1000)
    ticketNo = models.CharField(max_length=40, blank=True, null=True)
    reverseTax = models.BooleanField(default=False)
    invoiceAmount = models.FloatField(default=0.0)
    invoiceAmountWithTax = models.FloatField(default=0.0)
    paid = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    cancelReason = models.CharField(max_length=1000, blank=True, default="")
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    createdBy = models.EmailField(blank=True)
    
    def __str__(self):
        return self.invoiceId
    


class InvoiceProductLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invProdCode = models.CharField(max_length=20, blank=True)
    invProdName = models.CharField(max_length=50)
    invProdDescription = models.CharField(max_length=50, blank=True, default="")
    invProdHsnCode = models.CharField(max_length=20, blank=True, default="")
    invProdUom = models.CharField(max_length=5, default="")
    invProdQty = models.FloatField(default=0.0)
    invProdRate = models.FloatField(default=0.0)
    invProdLineAmount = models.FloatField(default=0.0)


class InvoiceTax(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    taxName = models.CharField(max_length=20, blank=True)
    taxPercent = models.FloatField(default=0.0, blank=True)


class CustomerSaleOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    saleOrder = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)


class CustomerInvoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)


class SaleOrderInvoice(models.Model):
    saleOrder = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)


class Payment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    mode = models.TextField(default="UPI", max_length=20)
    refUtrChequeNo = models.TextField(blank=True, null=True, max_length=100)
    bank = models.TextField(blank=True, null=True, max_length=100)
    paymentDate = models.DateField(blank=True, null=True)
    amount = models.FloatField(default=0.0, blank=True)
    remark = models.TextField(blank=True, null=True, max_length=100)
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    updatedOn = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.mode}|{self.amount}"


class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Outstanding(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dueAmount = models.FloatField(default=0.0, blank=True)
    totalBusinessAmount = models.FloatField(default=0.0, null=True, blank=True)
    createdOn = models.DateTimeField(default=today, null=True, blank=True)
    updatedOn = models.DateTimeField(default=today, null=True, blank=True)

    class Meta:
        verbose_name = "Outstanding"
        verbose_name_plural = "Outstandings"

    def __str__(self):
        return f"{self.customer} | {self.dueAmount}"