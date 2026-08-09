from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, ProductImage
from categories.models import Category
from reviews.models import Review

def catalog(request):
    """
    Product Catalog view supporting search, multi-facet filtering (category, price, rating, brand, availability),
    sorting, and pagination with optimized queries.
    """
    queryset = Product.objects.select_related('category').all()

    # Category Filter
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            # Include child categories if any
            child_ids = selected_category.children.values_list('id', flat=True)
            cat_ids = [selected_category.id] + list(child_ids)
            queryset = queryset.filter(category_id__in=cat_ids)

    # Search query
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )

    # Price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    # Rating filter
    min_rating = request.GET.get('rating')
    if min_rating:
        queryset = queryset.filter(rating_avg__gte=float(min_rating))

    # Brand filter
    brand = request.GET.get('brand')
    if brand:
        queryset = queryset.filter(brand__iexact=brand)

    # Flash Sale filter
    if request.GET.get('flash_sale') == 'true':
        queryset = queryset.filter(is_flash_sale=True)

    # Featured filter
    if request.GET.get('featured') == 'true':
        queryset = queryset.filter(is_featured=True)

    # Sorting
    sort_option = request.GET.get('sort', 'newest')
    if sort_option == 'price_low':
        queryset = queryset.order_by('price')
    elif sort_option == 'price_high':
        queryset = queryset.order_by('-price')
    elif sort_option == 'rating':
        queryset = queryset.order_by('-rating_avg')
    else:
        queryset = queryset.order_by('-created_at')

    # Aggregates for filter sidebar
    categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')
    brands = Product.objects.values_list('brand', flat=True).distinct()

    # Pagination
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'sort_option': sort_option,
        'query': query,
        'total_count': paginator.count,
    }
    return render(request, 'products/catalog.html', context)


def detail(request, slug):
    """
    Product Detail View with Gallery, Specifications, Reviews & Related Items.
    """
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Bundle item
    bought_together = Product.objects.exclude(id=product.id).order_by('?').first()
    
    reviews = product.reviews.select_related('user').all()

    context = {
        'product': product,
        'related_products': related_products,
        'bought_together': bought_together,
        'reviews': reviews,
    }
    return render(request, 'products/detail.html', context)


def search_suggest_api(request):
    """
    JSON API for navbar autocomplete search.
    """
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(title__icontains=query) | Q(brand__icontains=query)
    )[:5]

    results = []
    for p in products:
        results.append({
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'price': str(p.effective_price),
            'image': p.primary_image_url,
        })
    return JsonResponse({'results': results})


def quick_view_api(request, product_id):
    """
    JSON API for Quick View modal preview.
    """
    try:
        product = Product.objects.select_related('category').get(id=product_id)
        return JsonResponse({
            'success': True,
            'product': {
                'id': product.id,
                'title': product.title,
                'slug': product.slug,
                'price': str(product.effective_price),
                'image': product.primary_image_url,
                'description': product.short_description or product.description[:180],
                'category': product.category.name,
                'stock': product.stock,
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
