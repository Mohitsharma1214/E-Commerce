from django.shortcuts import render

def custom_404_view(request, exception):
    # Render the custom 404 page template
    return render(request, '404.html', status=404)
