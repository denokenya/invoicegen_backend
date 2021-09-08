from api.views import *
from purchase.serializers import *
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100000

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    # queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    def get_queryset(self):
        out = None
        data = self.request.query_params
        dateFrom = data.get("from")
        dateTo = data.get("to")
        if dateFrom and dateTo:
            out = PurchaseOrder.objects.filter(createdOn__date__range=[dateFrom, dateTo])
        else:
            out = PurchaseOrder.objects.all()
        return out

class PurchaseOrderProductViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderProduct.objects.all()
    serializer_class = PurchaseOrderProductSerializer

class PurchaseOrderTaxViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderTax.objects.all()
    serializer_class = PurchaseOrderTaxSerializer
