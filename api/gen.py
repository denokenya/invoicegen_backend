import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date
from django.db.models import Count
from sales.models import Invoice, SaleOrder
from account.models import *
from production.models import Product
from stock.models import RawMaterial
from sales.serializers import InvoiceSerializer, SaleOrderSerializer
from account.serializers import *
from production.serializers import ProductSerializer
from stock.serializers import RawMaterialSerializer


def jprint(d):
    return print(json.dumps(d, indent=4))


def formatint(n, leading_zeros_count=4):
    s = "{:0" + str(leading_zeros_count) + "}"
    return s.format(n)


def handleMask(mask, sep, data):
    mask = mask.replace("}{", "}" + sep + "{")
    return mask.format(**data)


def getTodayYearMonth():
    today = date.today()
    return [today, today.year, formatint(today.month, leading_zeros_count=2)]


ModelMapping = {
    "INVOICE": Invoice,
    "SALEORDER": SaleOrder,
    "CUSTOMER": Customer,
    "ADDRESS": Address,
    "PRODUCT": Product,
    "RAWMATERIAL": RawMaterial,
    # "EMPLOYEE": Employee,
    # "DRIVER": Driver,
    "VENDOR": Vendor,
}

SerializerMap = {
    "INVOICE": InvoiceSerializer,
    "SALEORDER": SaleOrderSerializer,
    "CUSTOMER": CustomerSerializer,
    "ADDRESS": AddressSerializer,
    "PRODUCT": ProductSerializer,
    # "EMPLOYEE": EmployeeSerializer,
    # "DRIVER": DriverSerializer,
    "RAWMATERIAL": RawMaterialSerializer,
    "VENDOR": VendorSerializer,
}

KeyName = {
    "INVOICE": "invoiceId",
    "SALEORDER": "saleOrderId",
    "CUSTOMER": "customerId",
    "ADDRESS": "code",
    "PRODUCT": "code",
    "EMPLOYEE": "code",
    "RAWMATERIAL": "code",
    "DRIVER": "code",
    "VENDOR": "code",
}


def saleorder_id_gen():
    today, year, month = getTodayYearMonth()
    total_so = formatint(len(SaleOrder.objects.filter(date__month=month)) + 1)
    mask = Ids.objects.filter(name="SALEORDER")[0]
    filler = {
        "year": year,
        "month": month,
        "count": total_so,
        "prefix": mask.prefix,
    }
    current = handleMask(mask.mask, mask.sep, filler)
    mask.current = current
    filler["count"] = formatint(int(filler["count"]) + 1)
    upnext = handleMask(mask.mask, mask.sep, filler)
    mask.upnext = upnext
    mask.save()
    return [current, upnext]


def customer_id_gen():
    today, year, month = getTodayYearMonth()
    total_so = formatint(len(Customer.objects.filter(date__month=month)) + 1)
    mask = Ids.objects.filter(name="CUSTOMER")[0]
    filler = {
        "year": year,
        "month": month,
        "count": total_so,
        "prefix": mask.prefix,
    }
    current = handleMask(mask.mask, mask.sep, filler)
    mask.current = current
    filler["count"] = formatint(int(filler["count"]) + 1)
    upnext = handleMask(mask.mask, mask.sep, filler)
    mask.upnext = upnext
    mask.save()
    return [current, upnext]


def invoice_no_gen():
    today, year, month = getTodayYearMonth()
    total_so = "00184"
    mask = Ids.objects.filter(name="INVOICE")[0]
    filler = {
        "year": year,
        "month": month,
        "count": total_so,
        "prefix": mask.prefix,
    }
    current = handleMask(mask.mask, mask.sep, filler)
    mask.current = current
    filler["count"] = formatint(int(filler["count"]) + 1)
    upnext = handleMask(mask.mask, mask.sep, filler)
    mask.upnext = upnext
    mask.save()
    return [current, upnext]


def genWithName(name, id=None, update=False, reset=False):
    today, year, month = getTodayYearMonth()
    model = ModelMapping[name]
    ids = []
    masks = Ids.objects.filter(name=name)
    if model.objects.count() == 0:
        total_so = formatint(1, leading_zeros_count=5 if name == "INVOICE" else 4)
    else:
        last = model.objects.last()
        if name == "EMPLOYEE":
            total_so = model.objects.count()
            total_so = formatint(
                (total_so if total_so == masks[0].count else masks[0].count) + 1,
                leading_zeros_count=4,
            )
        elif last.createdOn and last.createdOn.month == month:
            total_so = model.objects.values(KeyName[name]).last()[KeyName[name]][-4:]
            total_so = formatint(int(total_so) + 1, leading_zeros_count=4)
        else:
            if name == "PRODUCT":
                total_so = formatint(model.objects.count() + 1, leading_zeros_count=4)
            elif name == "INVOICE":
                total_so = formatint(masks[0].count + 1, leading_zeros_count=5)
            else:
                thismonthlength = len(model.objects.filter(createdOn__month=month))
                total_so = formatint(
                    (
                        thismonthlength
                        if thismonthlength == masks[0].count
                        else masks[0].count
                    )
                    + 1,
                    leading_zeros_count=4,
                )
    for mask in masks:
        filler = {
            "year": year,
            "month": month,
            "count": total_so,
            "prefix": mask.prefix,
        }
        current = handleMask(mask.mask, mask.sep, filler)
        mask.current = current
        filler["count"] = formatint(
            int(filler["count"]) + 1, 5 if name == "INVOICE" else 4
        )
        upnext = handleMask(mask.mask, mask.sep, filler)
        mask.upnext = upnext
        mask.save()
        ids.append([current, upnext])
    if update == False:
        return ids


@receiver(post_save)
def updateWithName(sender, instance, **kwargs):
    name = sender.__name__
    modelName = name.upper()
    for e in Ids.objects.filter(name=modelName):
        e.count = e.count + 1
        e.save()


def recalculateIds():
    l = list(ModelMapping.keys())
    for e in l:
        genWithName(e)
