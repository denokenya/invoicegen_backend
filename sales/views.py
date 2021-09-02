from rest_framework.pagination import PageNumberPagination
from api.views import *
from sales.serializers import *
from account.models import *
from account.serializers import CustomerSerializer

paginator = PageNumberPagination()
paginator.page_size = 50


class PaymentView(APIView):
    def get(self, request):
        data = request.query_params
        cid = data.get("id")
        fromDate = data.get("from")
        toDate = data.get("to")
        customerId = data.get("customerId")
        if cid:
            customer = Customer.objects.get(id=cid)
        if customerId:
            customer = Customer.objects.get(customerId=customerId)
        out = []
        if customer:
            if fromDate and toDate:
                customerpayments = CustomerPayment.objects.filter(customer=customer, paymentDate__range=[fromDate, toDate])
            else:
                customerpayments = CustomerPayment.objects.filter(customer=customer)
            if len(customerpayments) != 0:
                customerpayments = customerpayments.order_by("payment__paymentDate")
                payments = [cp.payment for cp in customerpayments]
                for e in PaymentSerializer(payments, many=True).data:
                    e["customer"] = CustomerSerializer(customer).data
                    out.append(e)
                return Response(data=out, status=201)
            else:
                return Response(data=[], status=201)
        else:
            return Response(data={"msg": "Customer Not Found"})

    def post(self, request):
        out = {}
        temp_payment = None
        try:
            data = request.data
            customer = Customer.objects.get(id=data["customer"]["id"])
            del data["customer"]
            if request.data["paymentDate"] == "":
                del request.data["paymentDate"]

            temp_payment = Payment(**data)
            serializer = PaymentSerializer(temp_payment)
            serializer = PaymentSerializer(data=serializer.data)
            valid = serializer.is_valid()
            if valid:
                temp_payment.save()
                outstanding = Outstanding.objects.filter(customer=customer)
                if len(outstanding) != 0:
                    outstanding = outstanding[0]
                    outstanding.totalBusinessAmount = (
                        outstanding.totalBusinessAmount or 0.0
                    )
                    outstanding.totalBusinessAmount = (
                        outstanding.totalBusinessAmount + temp_payment.amount
                    )
                    outstanding.dueAmount = outstanding.dueAmount - temp_payment.amount
                    outstanding.save()
                    out = PaymentSerializer(temp_payment).data
                    out["customer"] = CustomerSerializer(customer).data
                cp = CustomerPayment(customer=customer, payment=temp_payment)
                cp.save()
            return Response(data=out, status=201)
        except Exception as e:
            print(e)
            if temp_payment:
                cp = CustomerPayment.objects.filter(payment=temp_payment)[0].customer
                outstanding = cp.outstanding_set.last()

                outstanding.totalBusinessAmount = (
                    outstanding.totalBusinessAmount - temp_payment.amount
                )
                outstanding.dueAmount = outstanding.dueAmount + temp_payment.amount
                outstanding.save()
                temp_payment.delete()
            return Response(data={"msg": "Something Went Wrong"})

    def put(self, request, id):
        out = {}
        payment = Payment.objects.filter(id=id)
        if len(payment) == 0:
            return Response(data={}, status=404)
        else:
            payment = payment[0]
            serializer = PaymentSerializer(
                instance=payment, data=request.data, partial=True
            )
            valid = serializer.is_valid()
            if valid:
                serializer.save()
                out = serializer.data
                out["customer"] = CustomerSerializer(
                    CustomerPayment.objects.filter(payment=payment)[0].customer
                ).data
            else:
                out = serializer.errors
            return Response(data=out, status=201)

    def delete(self, request, id):
        out = {}
        payment = Payment.objects.filter(id=id)
        if payment.count() == 0:
            return Response(data={}, status=404)
        else:
            payment = payment[0]
            out = PaymentSerializer(payment).data
            cp = CustomerPayment.objects.filter(payment=payment)[0].customer
            outstanding = cp.outstanding_set.last()

            outstanding.totalBusinessAmount = (
                outstanding.totalBusinessAmount - payment.amount
            )
            outstanding.dueAmount = outstanding.dueAmount + payment.amount
            outstanding.save()
            payment.delete()
            return Response(data=out, status=201)


class SaleOrderViewSet(APIView):
    def get(self, request, id=None):
        out = []
        fromDate = request.query_params.get("from")
        toDate = request.query_params.get("to")
        asoptions = request.query_params.get("asoptions")
        if asoptions:
            so = SaleOrder.objects.filter(completed=False).order_by("-createdOn")
            for s in so:
                o = SaleOrderSerializer(s).data
                o["products"] = SaleOrderProductLineSerializer(
                    s.saleorderproductline_set.all(), many=True
                ).data
                o["taxes"] = SaleOrderTaxSerializer(
                    s.saleordertax_set.all(), many=True
                ).data
                out.append(o)
            out = {"results": out}
            return Response(data=out, status=201)
        if id:
            so = SaleOrder.objects.filter(id=id)
            if so.count() > 0:
                out = SaleOrderSerializer(so[0]).data
                out["products"] = SaleOrderProductLineSerializer(
                    so[0].saleorderproductline_set.all(), many=True
                ).data
                out["taxes"] = SaleOrderTaxSerializer(
                    so[0].saleordertax_set.all(), many=True
                ).data
                return Response(data=out, status=201)
            else:
                return Response(status=404)
        else:
            if fromDate and toDate:
                so = paginator.paginate_queryset(
                    SaleOrder.objects.filter(createdOn__range=[fromDate, toDate]).order_by("-createdOn"), request
                )
            else:
                so = paginator.paginate_queryset(
                    SaleOrder.objects.all().order_by("-createdOn"), request
                )
            for s in so:
                o = SaleOrderSerializer(s).data
                o["products"] = SaleOrderProductLineSerializer(
                    s.saleorderproductline_set.all(), many=True
                ).data
                o["taxes"] = SaleOrderTaxSerializer(
                    s.saleordertax_set.all(), many=True
                ).data
                out.append(o)
            pres = paginator.get_paginated_response(out)
            return pres

    def post(self, request):
        out = {}
        data = request.data
        products = data.get("products")
        taxes = data.get("taxes")
        del data["products"]
        del data["taxes"]
        if len(products) != 0:
            so = None
            try:
                data["createdOn"] = dt.now()
                soserializer = SaleOrderSerializer(data=data)
                valid = soserializer.is_valid()
                if valid:
                    so = SaleOrder.objects.create(**soserializer.data)
                    so.save()
                    out = SaleOrderSerializer(so).data
                    out["products"] = []
                    for product in products:
                        product["saleOrder"] = so
                        sop = SaleOrderProductLine(**product)
                        sop.save()
                        out["products"].append(SaleOrderProductLineSerializer(sop).data)
                    out["taxes"] = []
                    if len(taxes) == 0 or taxes == None:
                        taxes = Tax.objects.filter(use=True)
                    else:
                        taxes = [Tax.objects.get(id=tax) for tax in taxes]
                    for tax in taxes:
                        otax = {}
                        otax["saleOrder"] = so
                        otax["taxName"] = tax.code
                        otax["taxPercent"] = tax.percent
                        sot = SaleOrderTax(**otax)
                        sot.save()
                        out["taxes"].append(SaleOrderTaxSerializer(sot).data)

                    # adding saleorder to customer
                    cuso = CustomerSaleOrder(
                        saleOrder=so,
                        customer=Customer.objects.filter(customerId=so.customerId)[0],
                    )
                    cuso.save()
                    return Response(data=out, status=201)
                else:
                    return Response(
                        data={
                            "Err": "Something went wrong with saleorder",
                            "Details": soserializer.errors,
                        },
                        status=500,
                    )
            except Exception as e:
                so.delete()
                return Response(
                    data={
                        "message": e.__str__(),
                    },
                    status=500,
                )
        return Response(data=EXR, status=201)

    def put(self, request, id):
        pass

    def delete(self, request, id):
        so = SaleOrder.objects.filter(id=id)
        if so.count() > 0:
            so.delete()
            return Response(data={"msg": "OK"}, status=201)
        else:
            return Response(data={"msg": "Not Found"}, status=201)


class PlantSaleOrderViewSet(viewsets.ModelViewSet):
    queryset = PlantSaleOrder.objects.all()
    serializer_class = PlantSaleOrderSerializer


class InvoiceViewSet(APIView):
    def get(self, request):
        out = []
        id = request.query_params.get("invoiceId")
        fromDate = request.query_params.get("from")
        toDate = request.query_params.get("to")
        customerId = request.query_params.get("customerId")
        if id:
            inv = Invoice.objects.filter(invoiceId=id)
            if inv.count() > 0:
                out = InvoiceSerializer(inv[0]).data
                return Response(data=out, status=201)
            else:
                return Response(status=404)
        elif customerId:
            result_page = paginator.paginate_queryset(
                Invoice.objects.filter(customerId=customerId).order_by("createdOn"),
                request,
            )
            serializer = InvoiceSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            if fromDate and toDate:
                result_page = paginator.paginate_queryset(
                    Invoice.objects.filter(createdOn__range=[fromDate, toDate]).order_by("-createdOn"), request
                )
            else:
                result_page = paginator.paginate_queryset(
                    Invoice.objects.all().order_by("-createdOn"), request
                )
            serializer = InvoiceSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        products = data.get("invoiceProductData") or None
        del data["invoiceProductData"]
        if products is None:
            return Response(status=404)
        data["paid"] = data["paid"] or False
        data["cancelled"] = data["cancelled"] or False
        # del data["createdOn"]

        out = {}
        serialized = InvoiceSerializer(data=data)
        if serialized.is_valid():
            purged_data = serialized.validated_data
            inv = Invoice(**purged_data)
            inv.save()  # saving invoice
            out = InvoiceSerializer(inv).data

            [so] = SaleOrder.objects.filter(saleOrderId=inv.soNumber)  # get the so

            # resolve saleorder taxes to invoice taxes
            out["taxes"] = []
            sotaxes = so.saleordertax_set.all()
            for sotax in sotaxes:
                td = SaleOrderTaxSerializer(sotax).data
                del td["saleOrder"]
                del td["id"]
                td["invoice"] = inv
                invtax = InvoiceTax(**td)
                invtax.save()
                out["taxes"].append(InvoiceTaxSerializer(invtax).data)

            out["products"] = []
            # resolve invoice products
            allDone = True
            for product in products:
                pid = product["id"]
                del product["id"]
                product["invProdLineAmount"] = float(product["invProdLineAmount"])
                product["invoice"] = inv
                invprod = InvoiceProductLine(**product)
                invprod.save()
                sop = so.saleorderproductline_set.get(id=pid)
                r = sop.sopDeliveredQty + product["invProdQty"]
                if product["invProdQty"] <= sop.sopQty - sop.sopDeliveredQty:
                    sop.sopDeliveredQty = r
                    sop.save()
                else:
                    inv.delete()
                    return Response(
                        data={"msg": "Invalid invoice product qty"}, status=201
                    )
                out["products"].append(InvoiceProductLineSerializer(invprod).data)
                allDone = sop.sopQty == sop.sopDeliveredQty
            if allDone == True:
                so.completed = True
                so.completedOn = dt.now()
                so.save()
            # adding invoice to saleorder
            soinv = SaleOrderInvoice(invoice=inv, saleOrder=so)
            soinv.save()

            # adding invoice to customer
            cuinv = CustomerInvoice(
                invoice=inv,
                customer=Customer.objects.filter(customerId=inv.customerId)[0],
            )
            cuinv.save()
            return Response(data=out, status=201)
        else:
            return Response(data=serialized.errors, status=201)

    def put(self, request, id):
        pass

    def delete(self, request, id):
        print(id)
        inv = Invoice.objects.filter(id=id)
        if inv.count() > 0:
            inv = inv[0]
            so = SaleOrder.objects.filter(saleOrderId=inv.soNumber)[0]
            for p in inv.invoiceproductline_set.all():
                sop = so.saleorderproductline_set.filter(sopCode=p.invProdCode)[0]
                sop.sopDeliveredQty = sop.sopDeliveredQty - p.invProdQty
                so.completed = sop.sopDeliveredQty == sop.sopQty
                so.save()
                sop.save()
            inv.delete()
            return Response(
                data={
                    "invoiceId": inv.invoiceId,
                    "msg": f"Success: {inv.invoiceId} has been deleted.",
                },
                status=201,
            )
        else:
            return Response(data={"msg": "Not Found"}, status=201)


class OutstandingViewSet(APIView):
    def get(self, request, id=None):
        out = []
        cid = request.query_params.get("customer") or None
        if id:
            res = Outstanding.objects.filter(id=id)
            if cid:
                res = Outstanding.objects.filter(
                    id=id, customer=Customer.objects.get(id=cid)
                )
            if res.count() > 0:
                return Response(data=OutstandingSerializer(res[0]).data, status=201)
            else:
                return Response(status=404)
        if cid:
            res = Outstanding.objects.filter(customer__id=cid)
            customer = Customer.objects.get(id=cid)
            if res.count() > 0:
                res = res[0]
                recalc = request.query_params.get("recalculate") or False
                if recalc == "true":
                    customer = Customer.objects.get(id=cid)
                    dueAmount = customer.customerinvoice_set.filter(
                        invoice__paid=False
                    ).aggregate(Sum("invoice__invoiceAmountWithTax"))[
                        "invoice__invoiceAmountWithTax__sum"
                    ]
                    paidAmount = (
                        customer.customerpayment_set.all().aggregate(
                            Sum("payment__amount")
                        )["payment__amount__sum"]
                        or 0
                    )
                    res.dueAmount = dueAmount - paidAmount
                    res.totalBusinessAmount = paidAmount
                    res.save()
                out = OutstandingSerializer(res).data
                out["soCount"] = customer.customersaleorder_set.count()
                out["invoiceCount"] = customer.customerinvoice_set.count()
                return Response(data=out, status=201)
            else:
                dueAmount = (
                    customer.customerinvoice_set.filter(invoice__paid=False).aggregate(
                        Sum("invoice__invoiceAmountWithTax")
                    )["invoice__invoiceAmountWithTax__sum"]
                    or 0.0
                )
                totalBusinessAmount = (
                    customer.customerinvoice_set.filter(invoice__paid=True).aggregate(
                        Sum("invoice__invoiceAmountWithTax")
                    )["invoice__invoiceAmountWithTax__sum"]
                    or 0.0
                )
                cos = Outstanding(
                    customer=customer,
                    dueAmount=dueAmount,
                    totalBusinessAmount=totalBusinessAmount,
                )
                cos.save()
                out = OutstandingSerializer(cos).data
                out["soCount"] = customer.customersaleorder_set.count()
                out["invoiceCount"] = customer.customerinvoice_set.count()
                return Response(data=out, status=201)
        else:
            return Response(
                data=OutstandingSerializer(Outstanding.objects.all(), many=True).data,
                status=201,
            )
