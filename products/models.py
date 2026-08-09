from django.db import models
from django.utils.text import slugify
from categories.models import Category

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=280)
    sku = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100, default="NexCart Select")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=10)
    primary_image_url = models.URLField(max_length=500, help_text="Main product display image")
    
    # Badges & Flags
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_flash_sale = models.BooleanField(default=False)
    flash_sale_end = models.DateTimeField(null=True, blank=True)
    
    # Aggregates
    rating_avg = models.FloatField(default=4.8)
    rating_count = models.PositiveIntegerField(default=12)
    
    # Specifications (stored as JSON string or key/value pairs)
    specifications = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        if self.discount_price and self.price > self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def savings_amount(self):
        if self.discount_price and self.price > self.discount_price:
            return round(float(self.price - self.discount_price), 2)
        return 0.00

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price


    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.title}"
