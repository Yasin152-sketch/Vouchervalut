from django.db import models
from django.contrib.auth.models import User

class Voucher(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('CLAIMED', 'Claimed'),
    )

    brand = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    encrypted_code = models.TextField(help_text="AES-256 encrypted voucher code")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', db_index=True)
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_vouchers')
    claimed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} - {self.title} ({self.status})"

