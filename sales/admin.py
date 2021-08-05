from django.contrib import admin
from sales.models import Invoice, Outstanding, Payment, SaleOrder

admin.site.register(SaleOrder)
admin.site.register(Invoice)
admin.site.register(Outstanding)
admin.site.register(Payment)