from api.views import *
from stock.serializers import *
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100000

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer


class StockEntryViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = StockEntry.objects.all()
    serializer_class = StockEntrySerializer
