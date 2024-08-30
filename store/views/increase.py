from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from store.models.product import Products
from django.http import HttpRequest
from store.models.coupon import Coupon

class increase(View):
    def post(self, request: HttpRequest):
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')  # Action to perform: 'remove' or 'increase'

        if product_id:
            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                messages.error(request, "Product not found.")
                return redirect(request.POST.get('next', 'homepage'))

            size = request.POST.get('size')  # Get the selected size from the form
            print('size',size)
            # Construct a unique key for the cart entry considering both product and size
            cart_key = f"{product_id}-{size}"
            print(cart_key)

            cart = request.session.get('cart', {})
            if action == 'remove':
                if cart_key in cart:
                    cart.pop(cart_key)  # Remove product with the specified size from the cart
                    request.session['cart'] = cart
                    recalculate_total_cart_price(request)
                    messages.success(request, f"{product.name} ({size}) removed from your cart.")
                else:
                    messages.error(request, "Product not found in cart.")
            elif action == 'increase':
                cart[cart_key] = cart.get(cart_key, 0) + 1  # Increase product quantity in the cart
                request.session['cart'] = cart
                recalculate_total_cart_price(request)
                messages.success(request, f"Quantity of {product.name} ({size}) increased in your cart.")
            elif action == 'decrease':
                if cart_key in cart:
                    if cart[cart_key] > 1:
                        cart[cart_key] -= 1  # Decrease product quantity in the cart
                        request.session['cart'] = cart
                        recalculate_total_cart_price(request)
                        messages.success(request, f"Quantity of {product.name} ({size}) decreased in your cart.")
                    else:
                        cart.pop(cart_key)  # Remove product with the specified size from the cart if quantity becomes 0
                        request.session['cart'] = cart
                        recalculate_total_cart_price(request)
                        messages.success(request, f"{product.name} ({size}) removed from your cart.")
                else:
                    messages.error(request, "Product not found in cart.")
            else:
                messages.error(request, "Invalid action.")
            
            request.session['cart'] = cart
            recalculate_total_cart_price(request)

            return redirect(request.POST.get('next', 'homepage'))  # Redirect to the 'next' URL
        else:
            messages.error(request, "Invalid product ID.")
            return redirect(request.POST.get('next', 'homepage'))  # Redirect to the homepage if no product ID is provided

def recalculate_total_cart_price(request):
    cart = request.session.get('cart', {})
    applied_coupon = request.session.get('applied_coupon')
    total_price = calculate_total_cart_price(cart, applied_coupon)
    request.session['cart_total_price'] = total_price
    print('recalculated price:', total_price)

def calculate_total_cart_price(cart, coupon_code=None):
    total_price = 0
    for cart_key, quantity in cart.items():
        product_id, size = cart_key.split('-')  # Split the cart key to get product ID and size
        product = Products.objects.get(pk=product_id)
        total_price += product.price * quantity

    # Apply coupon discount if a coupon is provided
    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code)
        total_price -= (coupon.discount_percentage / 100) * total_price

    return int(total_price)
