from django.urls import path
from .views import VoucherListAPIView

urlpatterns = [
    path("", VoucherListAPIView.as_view(), name="voucher-list"),
]
