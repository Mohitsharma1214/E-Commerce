from django.shortcuts import redirect, render
from django.views import View
import razorpay
from store.models.customer import Customer
from store.models.orders import Order
from store.models.product import Products, Size
from store.models.coupon import Coupon
from store.models.address import Address

class CheckOut(View):
    def post(self, request):
        # Retrieve the address, new_address_text, and phone from the form submission
        address_id = request.POST.get('address')
        new_address_text = request.POST.get('new_address')
        phone = request.POST.get('phone')

        # Retrieve the customer ID from the session
        customer_id = request.session.get('customer')

        # Retrieve the cart data from the session
        cart = request.session.get('cart')

        # Retrieve applied coupon information
        applied_coupon = request.session.get('applied_coupon')
        coupon_discount = 0
        if applied_coupon:
            try:
                coupon = Coupon.objects.get(code=applied_coupon)
                coupon_discount = coupon.discount_percentage
            except Coupon.DoesNotExist:
                pass

        total_amount = 0  # Initialize total amount to zero

        # Create an empty list to store order details
        order_details = []

        # Calculate the total amount to be paid, considering product quantity and size
        for product_id, size in cart.items():
            # Split the product_id into product_id and size
            if isinstance(size, int):
                # Handle the case where size is an integer
                quantity = size
            else:
                quantity = cart[product_id][size]
            id_value = int(product_id.split('-')[0])
            id_value1 = int(product_id.split('-')[1])    
            product_id, size = product_id.split('-')

            # Retrieve the product from the database based on the product_id
            product = Products.objects.get(id=id_value)
            size = Size.objects.get(id=id_value1)

            

            
            print('size',size)
            if quantity > 0:
                total_amount += (product.price * quantity)
                # Append order details to the list
                order_details.append({
                    'product': product,
                    'quantity': quantity,
                    'size': size
                })
        
        # Apply coupon discount if applicable
        total_amount -= total_amount * coupon_discount / 100

        # Convert total amount to paise as an integer
        total_amount_in_paise = int(total_amount * 100)

        # Create an instance of the Razorpay client
        client = razorpay.Client(auth=('rzp_test_Hvfb0VmJQbUQ4m', 'gNXWArwdLKR4DNH9qt1soO8a'))

        # Create a Razorpay order
        order_currency = 'INR'
        order = client.order.create({
            'amount': total_amount_in_paise,
            'currency': order_currency,
        })

        # Get the logged-in customer object
        customer = Customer.objects.get(id=customer_id)

        # If neither an existing address is selected nor a new address is entered
        if not (address_id or new_address_text):
            return render(request, 'cart.html', {'error': 'Please select an existing address or enter a new one.'})

        # If an existing address is selected
        if address_id:
            # Get the corresponding address instance
            address = Address.objects.get(pk=address_id)
        # If a new address is entered
        elif new_address_text:
            # Create a new address instance
            address = Address.objects.create(customer=customer, address=new_address_text)
        
        # Save the order details in the database
        for order_detail in order_details:
            product = order_detail['product']
            quantity = order_detail['quantity']
            size = order_detail['size']
            new_order = Order.objects.create(
                customer=customer,
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=quantity,
                size=size,  # Save the size of the product
                razorpay_order_id=order['id']
            )

        # Clear the applied coupon after successful payment
        if applied_coupon:
            del request.session['applied_coupon']

        # Clear the cart after successful payment
        request.session['cart'] = {}

        # Redirect the user to the cart page
        return redirect('cart')
