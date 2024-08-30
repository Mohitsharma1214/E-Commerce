from django.shortcuts import render, redirect
from django.urls import reverse  # Import reverse to generate URL
from store.models.product import Products
from store.models.customerrating import Review
from store.models.customer import Customer
from django.contrib import messages 

def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Get the product instance
        product = Products.objects.get(pk=product_id)
        
        # Get the customer ID from the session
        customer_id = request.session.get('customer')
        
        if customer_id:
            # Retrieve the Customer instance corresponding to the customer ID
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                # Handle the case where the customer does not exist
                # For example, show an error message and redirect back to the product detail page
                login_url = reverse('login')  # Get the URL of the login page
                error_message = 'Please <a href="{}">log in</a> to submit a review.'.format(login_url)
                messages.error(request, error_message)
                return redirect('product-detail', product_id=product_id)  # Redirect to product detail with error message
        else:
            # If customer ID is not found in the session, ask the user to log in
            login_url = reverse('login')  # Get the URL of the login page
            error_message = 'Please <a href="{}">log in</a> to submit a review.'.format(login_url)
            messages.error(request, error_message)
            return redirect('product-detail', product_id=product_id)  # Redirect to product detail with error message
        
        # Create and save the review with the associated customer
        review = Review(product=product, customer=customer, rating=rating, comment=comment)
        review.save()
        
        return redirect('product-detail', product_id=product_id)  # Redirect to product detail after successful review submission
    else:
        return redirect('homepage')  # Redirect to home if not a POST request
