from django.shortcuts import render
from store.models.product import Products
from store.models.category import Category  # Import the Category model
from django.db.models import Q

from django.shortcuts import render
from store.models.product import Products
from store.models.category import Category
from django.http import JsonResponse
from django.db.models import Q

from django.http import JsonResponse
from store.models.product import Products
from store.models.category import Category
from django.db.models import Q

def SearchView(request):
    query = request.GET.get('q')
    suggestions = []

    if query:
        # Fetch suggestions based on product name, tag name, and category name
        product_suggestions = Products.objects.filter(name__icontains=query).values_list('name', flat=True)
        tag_suggestions = Products.objects.filter(tags__name__icontains=query).values_list('tags__name', flat=True)
        category_suggestions = Category.objects.filter(name__icontains=query).values_list('name', flat=True)

        suggestions = list(set(list(product_suggestions) + list(tag_suggestions) + list(category_suggestions)))

        # Return suggestions if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'suggestions': suggestions})

    categories = Category.objects.all()  # Fetch all categories
    results = None

    if query:
        # Perform the search query
        results = Products.objects.filter(
            Q(name__icontains=query) |     # Search by product name
            Q(tags__name__icontains=query) |   # Search by tag name
            Q(category__name__icontains=query)  # Search by category name
        ).distinct()

    return render(request, 'search_results.html', {'query': query, 'results': results, 'categories': categories})
