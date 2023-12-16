import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Max

from vendorapp.models import HistoricalPerformance, Vendor

@shared_task
def send_performance_email_to_vendors():
    # Get vendors
    vendors = Vendor.objects.all()

    # Iterate through vendors
    for vendor in vendors:
        # Get the latest historical performance record for the vendor
        latest_performance_data = HistoricalPerformance.objects.filter(
            vendor=vendor
        ).order_by('-date').first()

        # Prepare email content
        if latest_performance_data:
            subject = 'Latest Performance Report'
            message = f"Dear {vendor.name},\nHere is your latest performance report:\n\n"
            
            # Format the performance details
            performance_details = (
                f"Date: {latest_performance_data.date}\n"
                f"On-time Delivery Rate: {latest_performance_data.on_time_delivery_rate}\n"
                f"Quality Rating Average: {latest_performance_data.quality_rating_avg}\n"
                f"Average Response Time: {latest_performance_data.average_response_time}\n"
                f"Fulfillment Rate: {latest_performance_data.fulfillment_rate}\n"
            )

            # Append performance details to the message
            message += performance_details

            from_email = 'gauniyalutkarsh16@gmail.com'
            to_email = [vendor.email]

            # Send email
            send_mail(subject, message, from_email, to_email)