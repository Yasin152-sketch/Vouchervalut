# from django.urls import path
# from .views import OrderHealthCheckView
# from .views import VoucherCheckoutView, WalletDetailView

# urlpatterns = [
#     path("health/", OrderHealthCheckView.as_view(), name="order-health"),
#     path("wallet/", WalletDetailView.as_view(), name="wallet-detail"),
#     path("checkout/", VoucherCheckoutView.as_view(), name="voucher-checkout"),
# ]

from django.urls import path
from .views import VoucherCheckoutView, WalletDetailView, OrderHealthCheckView

urlpatterns = [
    path('health/', OrderHealthCheckView.as_view(), name='order-health'),
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path('checkout/', VoucherCheckoutView.as_view(), name='voucher-checkout'),
]