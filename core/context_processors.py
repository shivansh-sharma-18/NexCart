from categories.models import Category
from cart.models import Cart
from wishlist.models import Wishlist

def nexcart_context(request):
    """
    Global context processor supplying categories, cart count, wishlist count,
    and site metadata to all Django templates.
    """
    categories = []
    cart_count = 0
    wishlist_count = 0

    try:
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')[:8]
    except Exception:
        pass

    # Cart count
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart_count = sum(item.quantity for item in cart.items.all())
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
                if cart:
                    cart_count = sum(item.quantity for item in cart.items.all())
    except Exception:
        pass

    # Wishlist count
    try:
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user).first()
            if wishlist:
                wishlist_count = wishlist.items.count()
    except Exception:
        pass

    return {
        'nav_categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'site_name': 'NexCart',
        'site_tagline': 'Elevating Modern Commerce',
    }
