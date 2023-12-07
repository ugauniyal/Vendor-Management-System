from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, Vendor


# Signal handler for PurchaseOrder update
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.calculate_on_time_delivery_rate()
        instance.vendor.calculate_quality_rating_avg()
        instance.vendor.calculate_fulfillment_rate()


# Signal handler for PurchaseOrder acknowledgment
@receiver(pre_save, sender=PurchaseOrder)
def acknowledge_order(sender, instance, **kwargs):
    if instance.acknowledgment_date is None:
        instance.acknowledgment_date = timezone.now()
        instance.vendor.calculate_average_response_time()
