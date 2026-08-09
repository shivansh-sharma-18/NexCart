import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from django.contrib import messages
from orders.models import Order
from products.models import Product
from django.contrib.auth.models import User

@staff_member_required
def index(request):
    """
    Startup Admin & Seller Dashboard with KPI metric cards, SVG sales trend chart,
    low inventory alerts, and order status manager.
    """
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    avg_order_value = Order.objects.aggregate(Avg('total_amount'))['total_amount__avg'] or 0.00
    total_customers = User.objects.count()
    
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:8]
    low_stock_products = Product.objects.filter(stock__lte=5)
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': round(float(avg_order_value), 2),
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/index.html', context)


@staff_member_required
def update_order_status(request, order_id):
    """Fulfill or update order status via form POST"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.order_number} status updated to {order.get_status_display()}")
    return redirect('dashboard:index')


@staff_member_required
def update_order_status_api(request):
    """Fulfill or update order status via JSON API"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        order = get_object_or_404(Order, id=order_id)
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'message': f"Status updated to {order.get_status_display()}"})
        return JsonResponse({'success': False, 'message': 'Invalid status choice'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
