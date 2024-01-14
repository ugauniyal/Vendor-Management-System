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


from django.shortcuts import render

def home(request):
    api_info = [
        "### Get Token",
        "GET /api-token-auth/",
        "Pass the token in the headers to get authenticated. (Format - token 'your-token')",
        "",
        "### Vendor",
        "#### Get vendors list",
        "GET /api/vendors/",
        "Type: json",
        "Description: Get the vendor data response.",
        "",
        "#### Create vendor",
        "POST /api/vendors/",
        "Body: json",
        "Required fields: name, contact_details, address, vendor_code",
        "```json",
        "{",
        "  \"name\": \"name\",",
        "  \"contact_details\": \"contact_details\",",
        "  \"address\": \"address\",",
        "  \"vendor_code\": \"vendor_code\",",
        "  \"on_time_delivery_rate\": \"on_time_delivery_rate\",",
        "  \"quality_rating_avg\": \"quality_rating_avg\",",
        "  \"average_response_time\": \"average_response_time\",",
        "  \"fulfillment_rate\": \"fulfillment_rate\"",
        "}",
        "```",
        "",
        "#### Get specific vendor",
        "GET /api/vendors/{vendor_id}/",
        "Parameter: id (int) - Get the specific vendor data response.",
        "",
        "#### Get specific vendor performance",
        "GET /api/vendors/{vendor_id}/performance",
        "Parameter: id (int) - Get the specific vendor performance data response.",
        "",
        "#### Update Vendor",
        "PUT /api/vendors/{vendor_id}/",
        "Body: json",
        "Required fields: id, name, contact_details, address, vendor_code",
        "```json",
        "{",
        "  \"id\": 1,",
        "  \"name\": \"name\",",
        "  \"contact_details\": \"contact_details\",",
        "  \"address\": \"address\",",
        "  \"vendor_code\": \"vendor_code\",",
        "  \"on_time_delivery_rate\": \"on_time_delivery_rate\",",
        "  \"quality_rating_avg\": \"quality_rating_avg\",",
        "  \"average_response_time\": \"average_response_time\",",
        "  \"fulfillment_rate\": \"fulfillment_rate\"",
        "}",
        "```",
        "",
        "#### Delete Vendor",
        "DELETE /api/vendors/{vendor_id}/",
        "Parameter: id (int) - Delete the specific vendor.",
        "",
        "### Purchase Order",
        "#### Get purchase order list",
        "GET /api/purchase_orders/",
        "Type: json",
        "Description: Get all the purchase order data response.",
        "",
        "#### Create purchase order",
        "POST /api/purchase_orders/",
        "Body: json",
        "Required fields: po_number, order_date, delivery_date, items, quantity, status, quality_rating, issue_date, acknowledgment_date, vendor",
        "```json",
        "{",
        "  \"po_number\": \"po_number\",",
        "  \"order_date\": \"order_date\",",
        "  \"delivery_date\": \"delivery_date\",",
        "  \"items\": \"{ json data }\",",
        "  \"quantity\": \"quantity\",",
        "  \"status\": \"status\",",
        "  \"quality_rating\": \"quality_rating\",",
        "  \"issue_date\": \"issue_date\",",
        "  \"acknowledgment_date\": \"acknowledgment_date\",",
        "  \"vendor\": \"vendor_id\"",
        "}",
        "```",
        "",
        "#### Get specific purchase order",
        "GET /api/purchase_orders/{po_id}/",
        "Parameter: id (int) - Get the specific purchase order's data response.",
        "",
        "#### Update Purchase Order",
        "PUT /api/purchase_orders/{po_id}/",
        "Body: json",
        "Required fields: id, po_number, order_date, delivery_date, items, quantity, status, quality_rating, issue_date, acknowledgment_date, vendor",
        "```json",
        "{",
        "  \"id\": 1,",
        "  \"po_number\": \"po_number\",",
        "  \"order_date\": \"order_date\",",
        "  \"delivery_date\": \"delivery_date\",",
        "  \"items\": \"{ json data }\",",
        "  \"quantity\": \"quantity\",",
        "  \"status\": \"status\",",
        "  \"quality_rating\": \"quality_rating\",",
        "  \"issue_date\": \"issue_date\",",
        "  \"acknowledgment_date\": \"acknowledgment_date\",",
        "  \"vendor\": \"vendor_id\"",
        "}",
        "```",
        "",
        "#### Delete Purchase Order",
        "DELETE /api/purchase_orders/{po_id}/",
        "Parameter: id (int) - Delete the specific vendor.",
        "",
        "### Historical Performance",
        "GET /api/historical_performance/",
        "Type: json",
        "Description: Get the historical_performance of vendor.",
    ]

    return render(request, 'home.html', {'api_info': api_info})


