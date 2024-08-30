from django.shortcuts import render
from django.views import View

from store.models.category import Category
from store.models.orders import Order
from store.models.product import Products


class OrderView(View):
    def get(self, request):
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')

        if categoryID:
            products = Products.get_all_products_by_categoryid(categoryID)
        else:
            products = Products.get_all_products()
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        

        
        # Get sorting option from query parameters
        sort_option = request.GET.get('sort_option')

        # Default sorting by date
        orders = orders.order_by('-created_at')

        # Get distinct payment statuses present in the orders
        distinct_statuses = Order.objects.values_list('status', flat=True).distinct()

        # Generate sorting options for payment status
        payment_status_options = [('status_' + status.lower().replace(' ', '_'), status) for status in distinct_statuses]

        # Apply sorting based on sort_option
        if sort_option:
            if sort_option.startswith('status_'):
                status_to_sort = sort_option.split('_')[1].title()
                orders = orders.filter(status=status_to_sort)

        return render(request, 'orders.html', {'orders': orders, 'sort_option': sort_option, 'payment_status_options': payment_status_options,'categories':categories})
