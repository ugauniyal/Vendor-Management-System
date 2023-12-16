from django.contrib import admin

from vendorapp.models import HistoricalPerformance, PurchaseOrder, Vendor

# Register your models here.
admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)