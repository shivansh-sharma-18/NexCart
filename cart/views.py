import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from payments.models import Coupon

def get_or_create_cart(request):
    """Helper to get user or session-based cart"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


def view_cart(request):
    """Renders the shopping cart page"""
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all(),
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart_api(request):
    """AJAX JSON view to add product to cart with stock validation"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = max(1, int(data.get('quantity', 1)))

        product = get_object_or_404(Product, id=product_id)

        if product.stock <= 0:
            return JsonResponse({'success': False, 'message': f"'{product.title}' is currently out of stock."}, status=400)

        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        new_qty = (cart_item.quantity + quantity) if not created else quantity
        if new_qty > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            total_count = sum(item.quantity for item in cart.items.all())
            return JsonResponse({
                'success': True,
                'message': f"Limited to maximum available stock ({product.stock} units).",
                'cart_count': total_count
            })

        cart_item.quantity = new_qty
        cart_item.save()

        total_count = sum(item.quantity for item in cart.items.all())
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.title}' to cart!",
            'cart_count': total_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def update_cart_api(request):
    """AJAX JSON view to update cart item quantity or remove item"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        cart_item = get_object_or_404(CartItem, id=item_id)

        if quantity <= 0:
            cart_item.delete()
            message = "Item removed from cart"
        else:
            if quantity > cart_item.product.stock:
                quantity = cart_item.product.stock
                message = f"Quantity capped at available stock ({quantity})"
            else:
                message = "Cart updated"
            cart_item.quantity = quantity
            cart_item.save()

        cart = cart_item.cart if hasattr(cart_item, 'cart') else get_or_create_cart(request)
        total_count = sum(item.quantity for item in cart.items.all())

        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': total_count,
            'subtotal': str(cart.subtotal),
            'total': str(cart.total)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def apply_coupon(request):
    """Applies promo coupon to cart"""
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        cart = get_or_create_cart(request)

        if code in ['WELCOME10', 'NEXCART15', 'NEXCART20', 'LUXURY20']:
            discount = float(cart.subtotal) * 0.15
            cart.coupon_code = code
            cart.discount_amount = round(discount, 2)
            cart.save()
            messages.success(request, f"Coupon '{code}' applied! You saved ${cart.discount_amount}.")
        else:
            messages.error(request, "Invalid or expired coupon code. Try 'NEXCART15'!")

    return redirect('cart:view')
