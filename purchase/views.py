from api.views import *
from purchase.serializers import *
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100000

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderProductViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderProduct.objects.all()
    serializer_class = PurchaseOrderProductSerializer
