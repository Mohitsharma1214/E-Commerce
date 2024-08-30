from django import template

register = template.Library ()


@register.filter (name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys ()
    for id in keys:
        if int (id) == product.id:
            return True
    return False;

from django import template

register = template.Library()

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    if hasattr(product, 'size'):
        size = product.size.name  # Get the size of the product
    else:
        size = ''  # Set a default value if 'size' attribute is missing

    product_id = str(product.id)  # Convert product ID to string

    cart_key = f"{product_id}-{size}"  # Construct the cart key

    return cart.get(cart_key, 0)  # Get the quantity from the cart using the cart key


@register.filter (name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity (product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(product, cart):
    sum = 0
    for p in product:
        sum += p.price * cart_quantity(p, cart)
    return sum
