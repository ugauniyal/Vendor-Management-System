from rest_framework import generics, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorPerformanceSerializer, VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer




class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'pk'

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'


class HistoricalPerformanceListCreateView(generics.ListCreateAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer


class HistoricalPerformanceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    lookup_field = 'pk'



class VendorPerformanceView(generics.RetrieveAPIView):
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'pk'


    def get_queryset(self):
        vendor_id = self.kwargs['pk']
        return Vendor.objects.filter(id=vendor_id)

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        vendor.calculate_on_time_delivery_rate()
        vendor.calculate_quality_rating_avg()
        vendor.calculate_average_response_time()
        vendor.calculate_fulfillment_rate()
        serializer = self.get_serializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    serializer_class = PurchaseOrderSerializer


    def get_queryset(self):
        po_id = self.kwargs['pk']
        return PurchaseOrder.objects.filter(id=po_id)

    def put(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        purchase_order.acknowledge_order()
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
