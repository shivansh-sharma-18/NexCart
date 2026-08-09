from django.shortcuts import render
from products.models import Product
from categories.models import Category

def home(request):
    """
    Landing Page View: Hero, Featured Categories, Flash Sale,
    Trending Products, Best Sellers, Brand Grid, Testimonials & Stats.
    """
    featured_categories = Category.objects.filter(is_featured=True)[:6]
    if not featured_categories.exists():
        featured_categories = Category.objects.all()[:6]

    flash_sale_products = Product.objects.filter(is_flash_sale=True).select_related('category')[:4]
    if not flash_sale_products.exists():
        flash_sale_products = Product.objects.all().select_related('category')[:4]

    trending_products = Product.objects.filter(is_trending=True).select_related('category')[:8]
    if not trending_products.exists():
        trending_products = Product.objects.all().select_related('category')[:8]

    best_sellers = Product.objects.filter(is_best_seller=True).select_related('category')[:4]
    if not best_sellers.exists():
        best_sellers = Product.objects.all().select_related('category')[:4]

    context = {
        'categories': featured_categories,
        'featured_categories': featured_categories,
        'flash_sale_products': flash_sale_products,
        'trending_products': trending_products,
        'featured_products': trending_products,
        'best_sellers': best_sellers,
    }
    return render(request, 'core/index.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')
