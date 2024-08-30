# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import JsonResponse
from store.forms import NewsletterForm

from django.conf import settings
import requests
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import JsonResponse

from store.models.subsrciber import Subscriber
from django.conf import settings
import requests

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from store.models.subsrciber import Subscriber

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()

        # Validate email address
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Invalid email address!'}, status=400)

        if email:
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email)
                return JsonResponse({'message': 'Subscription successful!'})
            else:
                return JsonResponse({'error': 'Email already subscribed!'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid email!'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request!'}, status=400)
    
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from store.models.newsletter import Newsletter

@user_passes_test(lambda u: u.is_staff)

def send_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the newsletter to the database
            newsletter = Newsletter.objects.create(subject=subject, message=message)

            # Retrieve subscribers' email addresses
            subscribers = Subscriber.objects.values_list('email', flat=True)

            # Send the newsletter to subscribers
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, subscribers)

            return render(request, 'newsletter_sent.html')
    else:
        form = NewsletterForm()
    return render(request, 'send_newsletter.html', {'form': form})
