# from django.db import models
# from django.contrib.auth.models import User
# from vouchers.models import Voucher

# class IdempotencyLog(models.Model):
#     """
#     Rapid double-click aur duplicate requests ko rokkne ke liye cache table.
#     """
#     idempotency_key = models.CharField(max_length=120, unique=True, db_index=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='idempotency_logs')
#     response_body = models.JSONField(help_text="Cached API response for duplicate request replays")
#     status_code = models.PositiveIntegerField(default=200)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Idempotency Log"
#         verbose_name_plural = "Idempotency Logs"
#         ordering = ['-created_at']

#     def __str__(self):
#         username = self.user.username if self.user else "Anonymous"
#         return f"{self.idempotency_key[:12]}... | {username} | Status: {self.status_code}"


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('PENDING', 'Pending'),
#         ('COMPLETED', 'Completed'),
#         ('FAILED', 'Failed'),
#     )

#     order_id = models.CharField(max_length=50, unique=True, db_index=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, related_name='orders')
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
#     idempotency_key = models.CharField(max_length=120, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.order_id} - {self.user.username} (₹{self.amount_paid})"

# from django.db import models
# from django.contrib.auth.models import User
# from vouchers.models import Voucher
# import uuid
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from vouchers.models import Voucher


# class IdempotencyLog(models.Model):
#     idempotency_key = models.CharField(max_length=120, unique=True, db_index=True)
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="idempotency_logs",
#     )
#     response_body = models.JSONField(
#         help_text="Duplicate clicks par cache response bhejne ke liye"
#     )
#     status_code = models.PositiveIntegerField(default=200)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Idempotency Log"
#         verbose_name_plural = "Idempotency Logs"
#         ordering = ["-created_at"]

#     def __str__(self):
#         username = self.user.username if self.user else "Anonymous"
#         return (
#             f"{self.idempotency_key[:12]}... | {username} | Status: {self.status_code}"
#         )


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ("PENDING", "Pending"),
#         ("COMPLETED", "Completed"),
#         ("FAILED", "Failed"),
#     )

#     order_id = models.CharField(max_length=50, unique=True, db_index=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
#     voucher = models.ForeignKey(
#         Voucher, on_delete=models.PROTECT, related_name="orders"
#     )
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default="COMPLETED"
#     )
#     idempotency_key = models.CharField(max_length=120, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"{self.order_id} - {self.user.username} (₹{self.amount_paid})"


# class Wallet(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "User Wallet"
#         verbose_name_plural = "User Wallets"

#     def __str__(self):
#         return f"{self.user.username} | Balance: ₹{self.balance}"


# # Naya user bante hi automatically ₹5,000 fake money credit ho jayega
# @receiver(post_save, sender=User)
# def create_user_wallet(sender, instance, created, **kwargs):
#     if created:
#         Wallet.objects.create(user=instance, balance=5000.00)


# class IdempotencyLog(models.Model):
#     idempotency_key = models.CharField(max_length=120, unique=True, db_index=True)
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="idempotency_logs",
#     )
#     response_body = models.JSONField(
#         help_text="Cached API response for duplicate requests"
#     )
#     status_code = models.PositiveIntegerField(default=200)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Idempotency Log"
#         verbose_name_plural = "Idempotency Logs"
#         ordering = ["-created_at"]

#     def __str__(self):
#         username = self.user.username if self.user else "Anonymous"
#         return (
#             f"{self.idempotency_key[:12]}... | {username} | Status: {self.status_code}"
#         )


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ("PENDING", "Pending"),
#         ("COMPLETED", "Completed"),
#         ("FAILED", "Failed"),
#     )

#     order_id = models.CharField(max_length=50, unique=True, db_index=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
#     voucher = models.ForeignKey(
#         Voucher, on_delete=models.PROTECT, related_name="orders"
#     )
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(
#         max_length=20, choices=STATUS_CHOICES, default="COMPLETED"
#     )
#     idempotency_key = models.CharField(max_length=120, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"{self.order_id} - {self.user.username} (₹{self.amount_paid})"

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from vouchers.models import Voucher


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Wallet"
        verbose_name_plural = "User Wallets"

    def __str__(self):
        return f"{self.user.username} | Balance: ₹{self.balance}"


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=5000.00)


class IdempotencyLog(models.Model):
    idempotency_key = models.CharField(max_length=120, unique=True, db_index=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="idempotency_logs",
    )
    response_body = models.JSONField(
        help_text="Cached API response for duplicate requests"
    )
    status_code = models.PositiveIntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Idempotency Log"
        verbose_name_plural = "Idempotency Logs"
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return (
            f"{self.idempotency_key[:12]}... | {username} | Status: {self.status_code}"
        )


class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    )

    order_id = models.CharField(max_length=50, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    voucher = models.ForeignKey(
        Voucher, on_delete=models.PROTECT, related_name="orders"
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="COMPLETED"
    )
    idempotency_key = models.CharField(max_length=120, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_id} - {self.user.username} (₹{self.amount_paid})"
