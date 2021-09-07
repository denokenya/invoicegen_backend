from rest_framework import serializers
from purchase.models import *

class PurchaseOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderProduct
        fields = "__all__"

class PurchaseOrderSerializer(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()
    def get__materials(self, obj):
        if obj.purchaseorderproduct_set.count() > 0:
            return PurchaseOrderProductSerializer(
                obj.purchaseorderproduct_set.all(), many=True
            ).data
        else:
            return []
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
    

