from rest_framework import serializers
from .models import Voucher


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        # encrypted_code buyer ko display nahi karenge, sirf claimed hone par decrypt hoga
        fields = [
            "id",
            "brand",
            "title",
            "original_price",
            "sale_price",
            "status",
            "created_at",
        ]
