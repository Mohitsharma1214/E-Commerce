from django.shortcuts import render
from django.views import View
from store.models.address import Address
from store.models.category import Category
from store.models.customer import Customer
from store.models.product import Products, Size
from django.contrib.auth.models import User  # Import the User model

class Cart(View):
    
    def get(self, request):
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')

        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()
        
        # Ensure that cart data is set in the session
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        # Get products based on the product IDs and sizes in the cart
        cart = request.session['cart']
        items = []
        total_cart_price = 0  # Initialize total cart price
        
        for product_id, size in cart.items():
            if isinstance(size, int):
                # Handle the case where size is an integer
                quantity = size
            else:
                quantity = cart[product_id][size]
            
            # Split the product_id string and extract the part before the hyphen
            id_value = int(product_id.split('-')[0])
            id_value1 = product_id.split('-')[1]
            print('size',size)
            # Query the database using the integer ID
            product = Products.objects.get(id=id_value)
            size=Size.objects.get(id=id_value1)
            
                        
            
            # Calculate total price for the item
            total_price = product.price * quantity
            
            total_cart_price += total_price  # Add total price of the item to the total cart price
            
            items.append({
                'product': product,
                'size': size,    
                'quantity': quantity,
                'total_price': total_price  # Add total price attribute to the item
            })
        
        # Get the logged-in user's username
        username = request.user.username if request.user.is_authenticated else None
        customer_id = self.request.session.get('customer')
        if customer_id:
            customer = Customer.objects.get(pk=customer_id)
            customer_name = customer.username
            customer_email = customer.email
            customer_phone = customer.phone
            addresses = Address.objects.filter(customer_id=customer_id)
        else:
            addresses = None
        
        context = {
            'items': items,
            'username': username,
            'customer_name': customer_name,
            'categories': categories,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'cart': cart, 
            'addresses': addresses,
            'total_cart_price': total_cart_price  # Add total cart price to context
        }
        return render(request, 'cart.html', context)


# views.py
from django.http import JsonResponse

def cart_count(request):
    cart_count = len(request.session.get('cart', {}))
    return JsonResponse({'count': cart_count})
