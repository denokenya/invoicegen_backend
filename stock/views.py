from api.views import *
from stock.serializers import *


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer


class RawMaterialEntryViewSet(viewsets.ModelViewSet):

    queryset = RawMaterialEntry.objects.all()
    serializer_class = RawMaterialEntrySerializer
