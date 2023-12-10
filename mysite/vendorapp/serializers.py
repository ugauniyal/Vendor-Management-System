from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


# Serialize the data for vendor model including all the fields
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


# Serialize the data for PurchaseOrder model including all the fields
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'



# Serialize the data for PurchaseOrder model including all the fields for the acknowledge order endpoint.
class AcknowledgePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ()


# Serialize the data for HistoricalPerformance model including the performance of the vendor.
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)

    class Meta:
        model = HistoricalPerformance
        fields = (
            'vendor_name',
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate',
        )


# Serialize the data for vendor model including all the fields which determine the performance of the vendor.
class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate',
        )