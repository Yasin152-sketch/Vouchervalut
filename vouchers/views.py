from rest_framework import generics
from .models import Voucher
from .serializers import VoucherSerializer


class VoucherListAPIView(generics.ListAPIView):
    queryset = Voucher.objects.filter(status="AVAILABLE")
    serializer_class = VoucherSerializer


# Create your views here.
