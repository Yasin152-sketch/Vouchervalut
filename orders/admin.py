# from django.contrib import admin
# from .models import Order, IdempotencyLog

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_id', 'user', 'voucher', 'amount_paid', 'status', 'created_at')
#     list_filter = ('status', 'created_at')
#     search_fields = ('order_id', 'user__username', 'idempotency_key')
#     readonly_fields = ('created_at',)

# @admin.register(IdempotencyLog)
# class IdempotencyLogAdmin(admin.ModelAdmin):
#     list_display = ('idempotency_key', 'user', 'status_code', 'created_at')
#     search_fields = ('idempotency_key', 'user__username')
#     readonly_fields = ('created_at',)

# # Register your models here.


# from django.contrib import admin
# from .models import Order, IdempotencyLog


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         "order_id",
#         "user",
#         "voucher",
#         "amount_paid",
#         "status",
#         "created_at",
#     )
#     list_filter = ("status", "created_at")
#     search_fields = ("order_id", "user__username", "idempotency_key")
#     readonly_fields = ("created_at",)


# @admin.register(IdempotencyLog)
# class IdempotencyLogAdmin(admin.ModelAdmin):
#     list_display = ("idempotency_key", "user", "status_code", "created_at")
#     search_fields = ("idempotency_key", "user__username")
#     readonly_fields = ("created_at",)


# from django.contrib import admin
# from .models import Order, IdempotencyLog, Wallet

# @admin.register(Wallet)
# class WalletAdmin(admin.ModelAdmin):
#     list_display = ('user', 'balance', 'updated_at')
#     search_fields = ('user__username',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('order_id', 'user', 'voucher', 'amount_paid', 'status', 'created_at')
#     list_filter = ('status', 'created_at')
#     search_fields = ('order_id', 'user__username', 'idempotency_key')
#     readonly_fields = ('created_at',)

# @admin.register(IdempotencyLog)
# class IdempotencyLogAdmin(admin.ModelAdmin):
#     list_display = ('idempotency_key', 'user', 'status_code', 'created_at')
#     search_fields = ('idempotency_key', 'user__username')
#     readonly_fields = ('created_at',)

from django.contrib import admin
from .models import Order, IdempotencyLog, Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'updated_at')
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'voucher', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username', 'idempotency_key')
    readonly_fields = ('created_at',)

@admin.register(IdempotencyLog)
class IdempotencyLogAdmin(admin.ModelAdmin):
    list_display = ('idempotency_key', 'user', 'status_code', 'created_at')
    search_fields = ('idempotency_key', 'user__username')
    readonly_fields = ('created_at',)