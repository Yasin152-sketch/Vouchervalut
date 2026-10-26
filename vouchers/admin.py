from django.contrib import admin
from .models import Voucher


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "title",
        "sale_price",
        "status",
        "claimed_by",
        "created_at",
    )
    list_filter = ("status", "brand")
    search_fields = ("brand", "title")


# Register your models here.
