from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models.category import Category
from store.models.customerrating import Review
from store.models.product import Products
from django.utils import timezone

from django.db.models import Avg

from django.db.models import Avg
from decimal import Decimal

class ProductDetailView(View): 
    
    def get(self, request, product_id):
        # Get the requested product
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')

        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()

        product = get_object_or_404(Products, id=product_id)

        # Get related products
        related_products = product.get_related_products()
        sizes = product.sizes.all()
        print(sizes)
        # Get new drops (assuming new drops are products created within the last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        new_drops = Products.objects.filter(created_at__gte=seven_days_ago)
        product = Products.objects.get(pk=product_id)
        
        # Get reviews for the product along with customer information
        reviews = Review.objects.filter(product=product).select_related('customer')
        
        # Fetch filtered customer names who reviewed the product
        reviewers = reviews.values_list('customer__first_name', 'customer__last_name').distinct()
        
        # Calculate average rating
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg_rating is not None:
            avg_rating = Decimal(avg_rating).quantize(Decimal('1'))
            num_stars = int(avg_rating)
        else:
            avg_rating = None
            num_stars = 0
        
        # Capture recently viewed product
        viewed_products = request.session.get('viewed_products', [])
        if product_id not in viewed_products:
            viewed_products.append(product_id)
            request.session['viewed_products'] = viewed_products

        # Render the template with product details, related products, new drops, reviews, and average rating
        return render(request, 'product_detail.html', {
            'product': product,
            'related_products': related_products,
            'new_drops': new_drops,
            'categories': categories,
            'sizes':sizes,
            'reviews': reviews,
            'reviewers': reviewers,
            'avg_rating': avg_rating,
            'num_stars': num_stars
        })
