from django.db import models
from orders.models import Order

class PaymentTransaction(models.Model):
    PAYMENT_METHODS = (
        ('card', 'Credit / Debit Card'),
        ('upi', 'UPI / Instant Pay'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'NexCart Pay Wallet'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='card')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='SUCCESS')
    raw_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Order #{self.order.order_number}"


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.PositiveIntegerField(default=0, help_text="Percentage off e.g. 15 for 15%")
    fixed_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Flat amount off")
    min_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Coupon: {self.code}"
