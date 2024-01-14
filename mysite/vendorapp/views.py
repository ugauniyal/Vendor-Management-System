from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from vendorapp.tasks import send_performance_email_to_vendors
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import AcknowledgePurchaseOrderSerializer, VendorPerformanceSerializer, VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication


class VendorListCreateView(generics.ListCreateAPIView):
    # Handles GET (list) and POST (create) requests for Vendors
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # Handles GET (retrieve), PUT (update), and DELETE (destroy) requests for a Vendor
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'pk'


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    # Handles GET (list) and POST (create) requests for Purchase Orders
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # Handles GET (retrieve), PUT (update), and DELETE (destroy) requests for a Purchase Order
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'pk'


class HistoricalPerformanceListView(generics.ListAPIView):
    # Handles GET (list) requests for Historical Performances
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    


class VendorPerformanceView(generics.RetrieveAPIView):
    # Handles GET (retrieve) request for Vendor Performance
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        # Retrieve the requested vendor by ID
        vendor_id = self.kwargs.get('pk')
        if vendor_id is None:
            raise ValidationError("Vendor ID is required.")
        try:
            return Vendor.objects.filter(id=vendor_id)
        except Vendor.DoesNotExist:
            raise NotFound("Vendor not found.")

    def get(self, request, *args, **kwargs):
        try:
            # Retrieve and calculate vendor performance metrics
            vendor = self.get_object()
            vendor.calculate_on_time_delivery_rate()
            vendor.calculate_quality_rating_avg()
            vendor.calculate_average_response_time()
            vendor.calculate_fulfillment_rate()
            serializer = self.get_serializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any unexpected errors and return a 500 status code
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    serializer_class = AcknowledgePurchaseOrderSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        po_id = self.kwargs['pk']
        return PurchaseOrder.objects.filter(id=po_id)

    def put(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        purchase_order.acknowledge_order()  # Update acknowledgment_date
        return Response({"message": "Acknowledgment date updated"})


@api_view()
def trigger_performance_email(request):
    send_performance_email_to_vendors.delay()
    return Response({"message": "Performance email task triggered successfully."})



def home(request):
    # Provide a simple explanation of the available APIs
    api_info = [
        "1. GET/POST /api/vendors/ - List/Create Vendors",
        "2. GET/PUT/DELETE /api/vendors/<int:pk>/ - Retrieve/Update/Delete Vendor",
        "3. GET/POST /api/purchase_orders/ - List/Create Purchase Orders",
        "4. GET/PUT/DELETE /api/purchase_orders/<int:pk>/ - Retrieve/Update/Delete Purchase Order",
        "5. GET /api/historical_performance/ - List Historical Performances",
        "6. GET /api/vendors/<int:pk>/performance/ - Retrieve Vendor Performance Metrics",
        "7. PUT /api/purchase_orders/<int:pk>/acknowledge/ - Acknowledge Purchase Order",
        "8. GET /trigger-performance-email/ - Trigger Performance Email Task",
    ]

    api_info_with_line_breaks = "\n".join(api_info)

    return JsonResponse({'api_info': api_info_with_line_breaks}, safe=False)