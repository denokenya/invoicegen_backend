from rest_framework import serializers
from purchase.models import *

class PurchaseOrderTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderTax
        fields = "__all__"

class PurchaseOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderProduct
        fields = "__all__"

class PurchaseOrderSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()
    taxes = serializers.SerializerMethodField()
    
    def get__materials(self, obj):
        if obj.purchaseorderproduct_set.count() > 0:
            return PurchaseOrderProductSerializer(
                obj.purchaseorderproduct_set.all(), many=True
            ).data
        else:
            return []
    def get__taxes(self, obj):
        if obj.purchaseordertax_set.count() > 0:
            return PurchaseOrderTaxSerializer(
                obj.purchaseordertax_set.all(), many=True
            ).data
        else:
            return []
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
    

