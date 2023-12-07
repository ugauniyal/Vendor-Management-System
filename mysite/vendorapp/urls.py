from django.urls import path
from vendorapp.views import (
    AcknowledgePurchaseOrderView,
    VendorListCreateView,
    VendorPerformanceView,
    VendorRetrieveUpdateDestroyView,
    PurchaseOrderListCreateView,
    PurchaseOrderRetrieveUpdateDestroyView,
    HistoricalPerformanceListCreateView,
    HistoricalPerformanceRetrieveUpdateDestroyView,
)
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('api/historical_performance/', HistoricalPerformanceListCreateView.as_view(), name='historical-performance-list-create'),
    path('api/historical_performance/<int:pk>/', HistoricalPerformanceRetrieveUpdateDestroyView.as_view(), name='historical-performance-retrieve-update-destroy'),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
    # path('api/token/', obtain_auth_token, name='token_obtain_pair'),
]