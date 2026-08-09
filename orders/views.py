from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from orders.models import Order, OrderItem, OrderTracking
from payments.models import PaymentTransaction
from accounts.models import Address

@login_required
def checkout_view(request):
    """
    Multi-step Checkout View: Shipping Address, Payment Method & Order Review.
    Validates inventory stock and atomically decrements product inventory.
    """
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('products:catalog')

    cart_items = cart.items.select_related('product').all()
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('products:catalog')

    user_addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        shipping_name = request.POST.get('full_name', '').strip()
        shipping_phone = request.POST.get('phone', '').strip()
        shipping_street = request.POST.get('street_address', '').strip()
        shipping_city = request.POST.get('city', '').strip()
        shipping_state = request.POST.get('state', '').strip()
        shipping_postal_code = request.POST.get('postal_code', '').strip()
        shipping_country = request.POST.get('country', 'United States').strip()
        payment_method = request.POST.get('payment_method', 'card')

        if not all([shipping_name, shipping_phone, shipping_street, shipping_city, shipping_state, shipping_postal_code]):
            messages.error(request, "Please fill in all required shipping address fields.")
            context = {
                'cart': cart,
                'cart_items': cart_items,
                'user_addresses': user_addresses,
            }
            return render(request, 'orders/checkout.html', context)

        # Validate stock availability
        for item in cart_items:
            if item.product.stock < item.quantity:
                messages.error(request, f"Sorry, '{item.product.title}' has only {item.product.stock} units remaining.")
                return redirect('cart:view')

        try:
            with transaction.atomic():
                # Create Order
                order = Order.objects.create(
                    user=request.user,
                    status='placed',
                    payment_status='paid',
                    subtotal=cart.subtotal,
                    tax=cart.estimated_tax,
                    shipping_fee=cart.shipping_fee,
                    discount_amount=cart.discount_amount,
                    total_amount=cart.total,
                    shipping_name=shipping_name,
                    shipping_phone=shipping_phone,
                    shipping_street=shipping_street,
                    shipping_city=shipping_city,
                    shipping_state=shipping_state,
                    shipping_postal_code=shipping_postal_code,
                    shipping_country=shipping_country
                )

                # Create Order Items and Decrement Stock
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_title=item.product.title,
                        product_image_url=item.product.primary_image_url,
                        price=item.product.effective_price,
                        quantity=item.quantity
                    )
                    # Decrement inventory stock
                    item.product.stock = max(0, item.product.stock - item.quantity)
                    item.product.save()

                # Create Tracking Event
                OrderTracking.objects.create(
                    order=order,
                    step_name="Order Confirmed",
                    description="Your order has been placed and received by our fulfillment center.",
                    is_completed=True
                )

                # Create Payment Transaction Record
                PaymentTransaction.objects.create(
                    order=order,
                    payment_method=payment_method,
                    transaction_id=f"NEX-TXN-{order.order_number}",
                    amount=order.total_amount,
                    status="SUCCESS"
                )

                # Clear Cart
                cart.items.all().delete()
                cart.discount_amount = 0
                cart.coupon_code = ""
                cart.save()

            messages.success(request, f"Order #{order.order_number} placed successfully!")
            return redirect('orders:success', order_number=order.order_number)
        except Exception as e:
            messages.error(request, f"Failed to place order: {str(e)}")
            return redirect('cart:view')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'user_addresses': user_addresses,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/success.html', {'order': order})
