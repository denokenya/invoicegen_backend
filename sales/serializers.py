from rest_framework import serializers
from sales.models import *


class SaleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrder
        fields = "__all__"


class SaleOrderProductLineSerializer(serializers.ModelSerializer):
    saleOrder = serializers.PrimaryKeyRelatedField(queryset=SaleOrder.objects.all())

    class Meta:
        model = SaleOrderProductLine
        fields = "__all__"


class SaleOrderTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrderTax
        fields = "__all__"


class InvoiceTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTax
        fields = "__all__"


class InvoiceProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProductLine
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    taxes = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = "__all__"

    def get_products(self, obj):
        if obj.invoiceproductline_set.count() > 0:
            return InvoiceProductLineSerializer(
                obj.invoiceproductline_set.all(), many=True
            ).data
        else:
            return {}

    def get_taxes(self, obj):
        if obj.invoicetax_set.count() > 0:
            return InvoiceTaxSerializer(obj.invoicetax_set.all(), many=True).data
        else:
            return {}


class OutstandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outstanding
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PlantSaleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantSaleOrder
        fields = "__all__"