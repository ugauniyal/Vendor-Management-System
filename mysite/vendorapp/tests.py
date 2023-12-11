from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.contrib.auth.models import User

class VendorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="TEST123",
            on_time_delivery_rate=0.8,
            quality_rating_avg=4.5,
            average_response_time=5.7,
            fulfillment_rate=0.9

        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        data = {
            "name": "New Vendor",
            "contact_details": "New Contact",
            "address": "New Address",
            "vendor_code": "NEW123",
            "on_time_delivery_rate": 0.75,
            "quality_rating_avg": 4.0,
            "average_response_time": 6.2,
            "fulfillment_rate": 0.85

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vendor_by_id(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Vendor")

    def test_update_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        updated_data = {
            "name": "Updated Vendor",
            "contact_details": "Updated Contact",
            "address": "Updated Address",
            "vendor_code": "UPDATED123",
            "on_time_delivery_rate": 0.85,
            "quality_rating_avg": 4.2,
            "average_response_time": 6.0,
            "fulfillment_rate": 0.88

        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existing_vendor(self):
        non_existing_pk = 100
        url = reverse('vendor-retrieve-update-destroy', kwargs={'pk': non_existing_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)




class PurchaseOrderTests(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()


        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="TEST123",
            on_time_delivery_rate=0.8,
            quality_rating_avg=4.5,
            average_response_time=5.7,
            fulfillment_rate=0.9

        )

        self.purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number="PO123",
            order_date="2023-12-31T12:00:00Z",
            delivery_date="2024-01-15T12:00:00Z",
            items = {
                "tablet": 1
            },
            quantity=0,
            status="pending",
            quality_rating=None,
            issue_date="2023-12-31T12:00:00Z",
            acknowledgment_date=None
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_create_purchase_order(self):
        url = reverse('purchase-order-list-create')
        data = {
            "po_number": "PO1234",
            "order_date": "2023-12-11T14:04:17.283Z",
            "delivery_date": "2023-12-11T14:04:17.283Z",
            "items": {
                "tablet": 1
            },
            "quantity": 1,
            "status": "pending",
            "quality_rating": None,
            "issue_date": "2023-12-11T14:04:17.283Z",
            "acknowledgment_date": None,
            "vendor": self.vendor.pk,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_purchase_order_by_id(self):
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], "PO123")


    def test_update_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
        updated_data = {
            "po_number": "PO1234",
            "order_date": "2023-12-11T14:04:17.283Z",
            "delivery_date": "2023-12-11T14:04:17.283Z",
            "items": {
                "tablet": 2
            },
            "quantity": 2,
            "status": "pending",
            "quality_rating": None,
            "issue_date": "2023-12-11T14:04:17.283Z",
            "acknowledgment_date": None,
            "vendor": self.vendor.pk,
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': self.purchase_order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existing_purchase_order(self):
        non_existing_pk = 100
        url = reverse('purchase-order-retrieve-update-destroy', kwargs={'pk': non_existing_pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_acknowledge_purchase_order(self):
        url = reverse('acknowledge-purchase-order', kwargs={'pk': self.purchase_order.pk})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_non_existing_purchase_order(self):
        non_existing_pk = 100
        url = reverse('acknowledge-purchase-order', kwargs={'pk': non_existing_pk})
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class HistoricalPerformanceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="TEST123",
            on_time_delivery_rate=0.8,
            quality_rating_avg=4.5,
            average_response_time=5.7,
            fulfillment_rate=0.9
        )

        self.historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date="2023-12-31T12:00:00Z",
            on_time_delivery_rate=0.8,
            quality_rating_avg=4.5,
            average_response_time=5.7,
            fulfillment_rate=0.9
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retrieve_historical_performance(self):
        url = reverse('historical-performance-list-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
