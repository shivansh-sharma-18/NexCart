from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=100, null=True, blank=True, unique=True)
    coupon_code = models.CharField(max_length=50, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} ({'User: ' + self.user.username if self.user else 'Guest: ' + str(self.session_key)})"

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def estimated_tax(self):
        return round(float(self.subtotal) * 0.08, 2)

    @property
    def shipping_fee(self):
        return 0.00 if self.subtotal > 150 or self.subtotal == 0 else 15.00

    @property
    def total(self):
        return max(0.0, float(self.subtotal) + self.estimated_tax + self.shipping_fee - float(self.discount_amount))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        return self.product.effective_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
