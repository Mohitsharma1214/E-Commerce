from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from store.models.product import Products

def redirect_to_product_name(request, product_id):
    # Fetch the product by ID
    product = get_object_or_404(Products, id=product_id)

    # Construct the URL using the product name
    product_name = product.name.lower().replace(' ', '-')  # Convert name to URL-friendly format
    new_url = reverse('product-detail', kwargs={'product_name': product_name})

    # Redirect to the new URL
    return HttpResponseRedirect(new_url)
