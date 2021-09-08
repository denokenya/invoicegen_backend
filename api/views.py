from django.db.models import Sum
import os, base64
import urllib.parse as uri
from datetime import date, datetime as dt
from django.db.models.functions import TruncMonth
from rest_framework import response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
import time, json
from api.gen import (
    formatint,
    genWithName,
    getTodayYearMonth,
    handleMask,
    recalculateIds,
)
from account.serializers import UserSerializer, EmployeeSerializer
from account.models import Ids, Employee
from sales.models import Invoice, Payment, SaleOrder
from sales.serializers import InvoiceSerializer, PaymentSerializer, SaleOrderSerializer

helper = lambda x: [print(e) for e in dir(x)]
EXR = {
    "message": "Something Went Wrong",
}
TODAY = date.today()


def jwt_response_payload_handler(token, user=None, request=None):
    if user.is_superuser:
        userObj = UserSerializer(user, context={"context": request}).data
    else:
        userObj = EmployeeSerializer(Employee.objects.get(id=user.id), context={"context": request}).data
    return {"token": token, "user": userObj}


def jprint(d):
    return print(json.dumps(d, indent=4))


def incrementCountFor(model):
    for ids in Ids.objects.filter(name=model):
        ids.count = ids.count + 1
        ids.save()


# @api_view(["POST"])
# def sendMail(request):
#     file = request.FILES["file"]
#     tfn = file.name
#     msg = None
#     to = request.data["to"]
#     subject = request.data["subject"]
#     body = request.data["body"]
#     sentmsg = {}
#     with open(tfn, "wb") as f:
#         f.write(file.file.getbuffer())
#         msg = create_message_with_attachment(
#             to,
#             subject,
#             body,
#             tfn,
#         )

#         sentmsg = send_message("me", msg)
#     os.remove(tfn)
#     return Response(data=sentmsg, status=201)


@api_view(["GET"])
def getLastFive(request):
    modelMap = {"INVOICE": Invoice, "SALEORDER": SaleOrder, "PAYMENT": Payment}
    serializerMap = {
        "INVOICE": InvoiceSerializer,
        "SALEORDER": SaleOrderSerializer,
        "PAYMENT": PaymentSerializer,
    }
    what = request.query_params.get("what")
    return Response(
        status=200,
        data=serializerMap[what](
            data=modelMap[what].objects.order_by("-createdOn")[:5], many=True
        ).data,
    )


@api_view(["GET"])
def graphData(request):
    out = {
        "labels": [],
        "data": [],
    }
    mp = {"INVOICE": Invoice, "SALEORDER": SaleOrder, "PAYMENT": Payment}
    dtmp = {
        "INVOICE": "invoiceAmountWithTax",
        "SALEORDER": "totalAmount",
        "PAYMENT": "amount",
    }
    lbKey = request.query_params.get("labelKey") or "createdOn"
    name = request.query_params.get("name") or "PAYMENT"
    dtKey = request.query_params.get("dataKey") or dtmp[name]
    vals = mp[name].objects.values(lbKey, dtKey)
    for val in vals:
        k = (
            val[lbKey].strftime("%m/%d/%Y, %H:%M:%S")
            if lbKey == "createdOn"
            else val[lbKey]
        )
        out["labels"].append(k)
        out["data"].append(val[dtKey])
    return Response(data=out, status=201)