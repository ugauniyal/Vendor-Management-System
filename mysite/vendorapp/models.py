from django.db import models
from django.db.models import Count, F, ExpressionWrapper, Avg
from django.utils import timezone

# Vendor model to store vendor information and performance metrics
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)  # Tracks the percentage of on-time deliveries
    quality_rating_avg = models.FloatField(default=0)  # Average rating of quality based on purchase orders
    average_response_time = models.FloatField(default=0)  # Average time taken to acknowledge purchase orders
    fulfillment_rate = models.FloatField(default=0)  # Percentage of purchase orders fulfilled successfully

    # Method to calculate on-time delivery rate for the vendor
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchase_orders.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = on_time_pos.count() / total_completed_pos if total_completed_pos > 0 else 0
        self.on_time_delivery_rate = on_time_delivery_rate
        self.save()

    # Method to calculate average quality rating for the vendor
    def calculate_quality_rating_avg(self):
        completed_pos_with_rating = self.purchase_orders.filter(status='completed', quality_rating__isnull=False)
        quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        self.quality_rating_avg = quality_rating_avg or 0
        self.save()

    # Method to calculate average response time for the vendor
    def calculate_average_response_time(self):
        ack_pos = self.purchase_orders.filter(status='completed', acknowledgment_date__isnull=False)
        response_time = ack_pos.annotate(
            time_diff=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=models.DurationField())
        ).aggregate(avg_time=Avg('time_diff'))['avg_time']
        self.average_response_time = response_time.total_seconds() if response_time else 0
        self.save()

    # Method to calculate fulfillment rate for the vendor
    def calculate_fulfillment_rate(self):
        total_pos = self.purchase_orders.count()
        completed_pos_without_issues = self.purchase_orders.filter(status='completed', quality_rating__isnull=True)
        fulfillment_rate = completed_pos_without_issues.count() / total_pos if total_pos > 0 else 0
        self.fulfillment_rate = fulfillment_rate
        self.save()

    def __str__(self):
        return self.name

# PurchaseOrder model to capture details of each purchase order
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()  # Details of items ordered
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    # Method to acknowledge a purchase order and calculate average response time for the vendor
    def acknowledge_order(self):
        if self.acknowledgment_date is None:
            self.acknowledgment_date = timezone.now()
            self.save()
            self.vendor.calculate_average_response_time()

    # Method to update the status of a purchase order and trigger related calculations
    def update_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.save()
            if new_status == 'completed':
                self.vendor.calculate_on_time_delivery_rate()
                self.vendor.calculate_quality_rating_avg()
                self.vendor.calculate_fulfillment_rate()

    

    def __str__(self):
        return f"PO {self.po_number} for {self.vendor.name}"

# HistoricalPerformance model to store historical data on vendor performance
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performance')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()  # Historical record of the on-time delivery rate
    quality_rating_avg = models.FloatField()  # Historical record of the quality rating average
    average_response_time = models.FloatField()  # Historical record of the average response time
    fulfillment_rate = models.FloatField()  # Historical record of the fulfillment rate

    def __str__(self):
        return f"{self.vendor.name} - Performance on {self.date}"
