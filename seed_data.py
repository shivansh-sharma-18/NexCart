# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexcart.settings')
# django.setup()

# from django.contrib.auth.models import User
# from categories.models import Category
# from products.models import Product, ProductImage
# from accounts.models import UserProfile, Address
# from reviews.models import Review
# from orders.models import Order, OrderItem, OrderTracking
# from wishlist.models import Wishlist, WishlistItem

# def run_seed():
#     print("🌱 Initializing NexCart database seeder...")

#     # 1. Create Superuser & Demo Customer
#     admin_user, _ = User.objects.get_or_create(username='admin', defaults={
#         'email': 'admin@nexcart.io',
#         'first_name': 'NexCart',
#         'last_name': 'Admin',
#         'is_staff': True,
#         'is_superuser': True
#     })
#     admin_user.set_password('admin123')
#     admin_user.save()

#     shopper_user, _ = User.objects.get_or_create(username='shopper', defaults={
#         'email': 'shopper@domain.com',
#         'first_name': 'Alex',
#         'last_name': 'Mercer'
#     })
#     shopper_user.set_password('shopper123')
#     shopper_user.save()

#     print("✅ Created demo users ('admin' / 'shopper').")

#     # 2. Create Categories
#     cat_data = [
#         {"name": "Electronics & Tech", "slug": "electronics", "is_featured": True},
#         {"name": "Audio & Sound", "slug": "audio", "is_featured": True},
#         {"name": "Designer Fashion", "slug": "fashion", "is_featured": True},
#         {"name": "Minimalist Home", "slug": "home-decor", "is_featured": True},
#         {"name": "Luxury Watches", "slug": "watches", "is_featured": True},
#     ]

#     cat_map = {}
#     for c in cat_data:
#         obj, _ = Category.objects.get_or_create(slug=c['slug'], defaults={
#             'name': c['name'],
#             'is_featured': c['is_featured']
#         })
#         cat_map[c['slug']] = obj

#     print("✅ Seeded main categories.")

#     # 3. Create Products
#     products_data = [
#         {
#             "title": "Aura Noise-Canceling Wireless Headphones",
#             "slug": "aura-noise-canceling-headphones",
#             "sku": "NEX-AUD-001",
#             "brand": "Aura Acoustic",
#             "category": cat_map['audio'],
#             "price": 349.99,
#             "discount_price": 299.99,
#             "stock": 18,
#             "primary_image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
#             "is_featured": True,
#             "is_trending": True,
#             "is_flash_sale": True,
#             "rating_avg": 4.9,
#             "rating_count": 48,
#             "description": "Engineered with titanium acoustic drivers and hybrid active noise cancellation. 40-hour battery stamina with wireless quick charging."
#         },
#         {
#             "title": "Chronos Automatic Titanium Timepiece",
#             "slug": "chronos-automatic-titanium-timepiece",
#             "sku": "NEX-WCH-002",
#             "brand": "Chronos Craft",
#             "category": cat_map['watches'],
#             "price": 890.00,
#             "discount_price": 750.00,
#             "stock": 6,
#             "primary_image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
#             "is_featured": True,
#             "is_best_seller": True,
#             "rating_avg": 5.0,
#             "rating_count": 32,
#             "description": "Swiss-inspired 24-jewel movement enclosed in grade-5 brushed titanium with anti-reflective sapphire crystal."
#         },
#         {
#             "title": "Vanguard Ultra-Thin Aluminum Laptop 15",
#             "slug": "vanguard-ultrathin-aluminum-laptop",
#             "sku": "NEX-LPT-003",
#             "brand": "Vanguard Tech",
#             "category": cat_map['electronics'],
#             "price": 1499.00,
#             "discount_price": 1349.00,
#             "stock": 12,
#             "primary_image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
#             "is_trending": True,
#             "rating_avg": 4.8,
#             "rating_count": 89,
#             "description": "M-Series 10-core architecture, Liquid Retina XDR display, and 18-hour battery housed in a seamless unibody aluminum shell."
#         },
#         {
#             "title": "Nordic Ambient Matte Ceramic Lamp",
#             "slug": "nordic-ambient-matte-ceramic-lamp",
#             "sku": "NEX-LMP-004",
#             "brand": "Nordic Studio",
#             "category": cat_map['home-decor'],
#             "price": 180.00,
#             "discount_price": 145.00,
#             "stock": 4, # Low stock trigger
#             "primary_image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80",
#             "is_flash_sale": True,
#             "rating_avg": 4.7,
#             "rating_count": 19,
#             "description": "Hand-thrown ceramic base with warm dimmable LED ambiance. Perfect for minimalist modern workspace lighting."
#         },
#         {
#             "title": "Atelier Italian Calfskin Travel Weekender",
#             "slug": "atelier-italian-calfskin-weekender",
#             "sku": "NEX-BAG-005",
#             "brand": "Atelier Milano",
#             "category": cat_map['fashion'],
#             "price": 620.00,
#             "discount_price": 540.00,
#             "stock": 15,
#             "primary_image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
#             "is_featured": True,
#             "rating_avg": 4.9,
#             "rating_count": 27,
#             "description": "Full-grain Tuscan leather with brass hardware and reinforced suede interior compartment."
#         },
#         {
#             "title": "Pulse OLED Smart Fitness Tracker",
#             "slug": "pulse-oled-smart-fitness-tracker",
#             "sku": "NEX-WRB-006",
#             "brand": "Pulse Labs",
#             "category": cat_map['electronics'],
#             "price": 220.00,
#             "discount_price": 189.00,
#             "stock": 25,
#             "primary_image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?auto=format&fit=crop&w=800&q=80",
#             "is_trending": True,
#             "rating_avg": 4.6,
#             "rating_count": 64,
#             "description": "Continuous ECG monitoring, sleep architecture tracking, and 50m water resistance with curved sapphire glass."
#         }
#     ]

#     for p in products_data:
#         obj, _ = Product.objects.update_or_create(slug=p['slug'], defaults=p)


#     print("✅ Seeded products with realistic imagery & specs.")

#     # 4. Create Demo Orders for Shopper
#     if not Order.objects.filter(user=shopper_user).exists():
#         prod = Product.objects.first()
#         order = Order.objects.create(
#             user=shopper_user,
#             status='shipped',
#             payment_status='paid',
#             subtotal=prod.effective_price,
#             tax=24.00,
#             shipping_fee=0.00,
#             total_amount=float(prod.effective_price) + 24.00,
#             shipping_name="Alex Mercer",
#             shipping_phone="+1 555-019-2834",
#             shipping_street="742 Evergreen Terrace",
#             shipping_city="San Francisco",
#             shipping_state="CA",
#             shipping_postal_code="94107",
#             shipping_country="United States"
#         )

#         OrderItem.objects.create(
#             order=order,
#             product=prod,
#             product_title=prod.title,
#             product_image_url=prod.primary_image_url,
#             price=prod.effective_price,
#             quantity=1
#         )
#         OrderTracking.objects.create(
#             order=order,
#             step_name="Order Placed",
#             description="Verified via NexCart Security",
#             is_completed=True
#         )
#         print("✅ Seeded demo orders and tracking history.")

#     # 5. Create Product Reviews
#     prod1 = Product.objects.first()
#     if prod1 and not Review.objects.filter(product=prod1).exists():
#         Review.objects.create(
#             product=prod1,
#             user=shopper_user,
#             rating=5,
#             headline="Exceptional Audio Clarity",
#             comment="The active noise canceling completely silences airplane engine hum. Audio stage is rich and warm."
#         )
#         print("✅ Seeded customer reviews.")

#     print("🚀 NexCart Database Seeding Completed Successfully!")

# if __name__ == '__main__':
#     run_seed()
