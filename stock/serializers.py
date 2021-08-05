from rest_framework import serializers
from stock.models import *


class RawMaterialEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialEntry
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = "__all__"