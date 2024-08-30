# views.py
from store.forms import ContactForm
from store.models.contact import ContactMessage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the form data to the ContactMessage model
            ContactMessage.objects.create(name=name, email=email, phone_number=phone_number, subject=subject, message=message)

            # Send email notification
            email_subject = 'New contact form submission: ' + subject
            email_body = f'Name: {name}\nEmail: {email}\nPhone Number: {phone_number}\nSubject: {subject}\nMessage: {message}'
            sender_email = 'ptms2525@gmail.com'  # Update this with your email address
            recipient_email = ['ptms2525@gmail.com']  # Update this with your email address or a list of recipients
            send_mail(email_subject, email_body, sender_email, recipient_email, fail_silently=True)

            # Return a success message in JSON format
            return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})
        else:
            # Return form errors in JSON format
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # If it's a GET request, render the form page
        form = ContactForm()
        return render(request, 'contact-form.html', {'form': form})
