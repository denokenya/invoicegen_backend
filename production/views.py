from rest_framework import viewsets
from production.models import *
from production.serializers import *
from datetime import date, datetime as dt

TODAY = date.today()


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
