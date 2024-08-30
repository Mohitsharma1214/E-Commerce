from time import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Products
from store.models.category import Category
from django.http import HttpResponseRedirect
from datetime import timedelta
from django.utils import timezone
class Index(View):

    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        # Fetch product object using product_id
        product = Products.objects.get(id=product_id)

        if cart:
            quantity = cart.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product_id)
                        messages.success(request, f"{product.name} removed from your cart.")
                    else:
                        cart[product_id] = quantity - 1
                        messages.success(request, f"One {product.name} removed from your cart.")
                else:
                    cart[product_id] = quantity + 1
                    messages.success(request, f"{product.name} added to your cart.")
            else:
                cart[product_id] = 1
                messages.success(request, f"{product.name} added to your cart.")
        else:
            cart = {product_id: 1}
            messages.success(request, f"{product.name} added to your cart.")

        request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


from django.shortcuts import render, redirect

from django.shortcuts import render
from store.models.category import Category
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist exception

def store(request):
    cart = request.session.get('cart', {})
    if not cart:
        request.session['cart'] = {}

    categories = Category.get_all_categories()
    category_id = request.GET.get('category')

    category_name = None  # Default value for category_name

    # Attempt to retrieve category name from database
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.name
        except ObjectDoesNotExist:
            category_name = None

    # Retrieve products based on the selected category
    if category_id:
        products = Products.get_all_products_by_categoryid(category_id)
        template = 'search.html'
    else:
        products = Products.get_all_products()
        template = 'index.html'

    # Retrieve other necessary data
    recently_viewed_ids = request.session.get('viewed_products', [])
    recently_viewed_products = Products.get_products_by_id(recently_viewed_ids)
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_drops = Products.objects.filter(created_at__gte=seven_days_ago)

    context = {
        'products': products,
        'categories': categories,
        'email': request.session.get('email'),
        'recently_viewed': recently_viewed_products,
        'new_drops': new_drops,
        'category_name': category_name,  # Pass category_name to the template
    }

    return render(request, template, context)
