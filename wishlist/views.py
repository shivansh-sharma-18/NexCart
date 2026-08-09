import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist, WishlistItem
from products.models import Product

def get_or_create_wishlist(user):
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


@login_required
def view_wishlist(request):
    wishlist = get_or_create_wishlist(request.user)
    items = wishlist.items.select_related('product').all()
    return render(request, 'wishlist/view.html', {'wishlist_items': items})


def toggle_wishlist_api(request):
    """AJAX JSON endpoint for adding/removing product from wishlist"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please sign in to save items to your wishlist.'}, status=401)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        wishlist = get_or_create_wishlist(request.user)
        item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()

        if item:
            item.delete()
            added = False
            msg = f"Removed '{product.title}' from wishlist"
        else:
            WishlistItem.objects.create(wishlist=wishlist, product=product)
            added = True
            msg = f"Saved '{product.title}' to wishlist!"

        count = wishlist.items.count()
        return JsonResponse({
            'success': True,
            'added': added,
            'message': msg,
            'wishlist_count': count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
