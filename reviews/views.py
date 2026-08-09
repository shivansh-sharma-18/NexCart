from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Review
from products.models import Product

@login_required
def add_review(request, product_id):
    """
    Allows authenticated users to post product reviews and automatically updates product rating average and count.
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 5))
        rating = max(1, min(5, rating))
        comment = request.POST.get('comment', '').strip()
        headline = request.POST.get('headline', '').strip()

        if not comment:
            messages.error(request, "Please enter a comment for your review.")
            return redirect('products:detail', slug=product.slug)

        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'headline': headline,
                'comment': comment,
                'is_verified_purchase': True
            }
        )

        # Recalculate rating stats
        aggregates = product.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
        product.rating_avg = round(float(aggregates['avg'] or 5.0), 1)
        product.rating_count = aggregates['count'] or 0
        product.save()

        messages.success(request, "Thank you! Your review has been published.")
        return redirect('products:detail', slug=product.slug)

    return redirect('core:home')
