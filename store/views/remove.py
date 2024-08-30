from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from store.models.coupon import Coupon
from store.models.product import Products, Size
from django.http import HttpRequest

class RemoveFromCart(View):
    def post(self, request: HttpRequest):
        product_id = request.POST.get('product_id')
        size_name = request.POST.get('size')
        print("Product ID:", product_id)
        print("Size Name:", size_name)

        action = request.POST.get('action')  # Action to perform: 'remove', 'increase', or 'decrease'

        if product_id and size_name:
            try:
                # Get the product and size objects
                product = Products.objects.get(id=product_id)
                size = Size.objects.get(name=size_name)
                # Extract size ID
                size_id = str(size.id).split('-')[0]
                size_id = int(size_id)
                print('size id', size_id)

                # Define the cart item key based on product ID and size
                cart_item_key = f"{product_id}-{size_id}"
                print(cart_item_key)

                # Get the cart from session
                cart = request.session.get('cart', {})

                if action == 'remove':
                    if cart_item_key in cart:
                        cart.pop(cart_item_key)  # Remove product from the cart
                        request.session['cart'] = cart
                        recalculate_total_cart_price(request)
                        messages.success(request, f"{product.name} ({size_name}) removed from your cart.")
                    else:
                        messages.error(request, "Product not found in cart.")
                elif action == 'increase':
                    if cart_item_key in cart:
                        cart[cart_item_key] += 1  # Increase product quantity in the cart
                        request.session['cart'] = cart
                        recalculate_total_cart_price(request)
                        messages.success(request, f"Quantity of {product.name} ({size_name}) increased in your cart.")
                    else:
                        messages.error(request, "Product not found in cart.")
                elif action == 'decrease':
                    if cart_item_key in cart:
                        if cart[cart_item_key] > 1:
                            cart[cart_item_key] -= 1  # Decrease product quantity in the cart
                            request.session['cart'] = cart
                            recalculate_total_cart_price(request)
                            messages.success(request, f"Quantity of {product.name} ({size_name}) decreased in your cart.")
                    else:
                        messages.error(request, "Product not found in cart.")
                else:
                    messages.error(request, "Invalid action.")
            except Products.DoesNotExist:
                messages.error(request, "Product does not exist.")
            except Size.DoesNotExist:
                messages.error(request, "Size does not exist.")
            except ValueError:
                messages.error(request, "Invalid size ID.")
        else:
            messages.error(request, "Invalid product ID or size.")

        return redirect('cart')  # Redirect to the cart page after performing the action

def recalculate_total_cart_price(request):
    cart = request.session.get('cart', {})
    applied_coupon = request.session.get('applied_coupon')
    total_price = calculate_total_cart_price(cart, applied_coupon)
    request.session['cart_total_price'] = total_price
    print('recalculated price:', total_price)

def calculate_total_cart_price(cart, coupon_code=None):
    total_price = 0
    for cart_item_key, quantity in cart.items():
        product_id, size_id = map(int, cart_item_key.split('-'))
        product = Products.objects.get(pk=product_id)
        total_price += product.price * quantity

    # Apply coupon discount if a coupon is provided
    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code)
        total_price -= (coupon.discount_percentage / 100) * total_price

    return int(total_price)
