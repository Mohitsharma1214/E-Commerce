from django.shortcuts import redirect
from django.views import View
from django.contrib import messages  # Import messages framework
from store.models.coupon import Coupon
from store.models.product import Products

from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from store.models.coupon import Coupon
from datetime import date

class ApplyCoupon(View):
    def post(self, request):
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code).first()
            if coupon:
                if coupon.expiry_date < date.today():
                    # Coupon has expired
                    messages.error(request, 'Coupon has expired!')
                else:
                    request.session['applied_coupon'] = coupon.code
                    messages.success(request, 'Coupon applied successfully!')
                    
                    # Recalculate total cart price after applying the coupon
                    cart = request.session.get('cart', {})
                    total_price = calculate_total_cart_price(cart, coupon.code)
                    request.session['cart_total_price'] = total_price
            else:
                messages.error(request, 'Invalid coupon code!')
                
        return redirect('cart')


def calculate_total_cart_price(cart, coupon_code=None):
    total_price = 0
    for cart_item in cart.items():
        product_id, quantity = cart_item
        id_value = int(product_id.split('-')[0])  # Extract the product ID
        product = Products.objects.get(pk=id_value)
        total_price += product.price * quantity

    # Apply coupon discount if a coupon is provided
    if coupon_code:
        coupon = Coupon.objects.get(code=coupon_code)
        total_price -= (coupon.discount_percentage / 100) * total_price

    return int(total_price)


class RemoveCoupon(View):
    def post(self, request):
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
            messages.success(request, 'Coupon removed successfully!')
            
            # Recalculate total cart price after removing the coupon
            cart = request.session.get('cart', {})
            total_price = calculate_total_cart_price(cart)
            request.session['cart_total_price'] = total_price
        return redirect('cart')
