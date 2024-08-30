# views.py

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models.customer import Customer


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils.http import base36_to_int, int_to_base36
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import constant_time_compare

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int, int_to_base36
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int, int_to_base36

class MyTokenGenerator(PasswordResetTokenGenerator):
    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

    def _make_hash_value(self, user, timestamp):
        """
        Generate a hash value for the user, timestamp, and some internal data.
        """
        if not user.pk:
            raise ValueError("User must have a primary key assigned to use 'MyTokenGenerator'.")

        # Use user's primary key instead of last_login
        return (
            str(user.pk) + user.password +
            str(timestamp)
        )

default_token_generator = MyTokenGenerator()


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Customer  # Assuming Customer is your user model

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Customer

class MyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.password +
            str(timestamp)
        )

default_token_generator = MyTokenGenerator()

from django.conf import settings
from django.http import HttpRequest

class PasswordResetRequestView(View):
    template_name = 'password_reset_request.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username_or_email = request.POST.get('username_or_email').lower()
        try:
            user = Customer.objects.get(email=username_or_email)
        except Customer.DoesNotExist:
            try:
                user = Customer.objects.get(username=username_or_email)
            except Customer.DoesNotExist:
                user = None

        if user is not None:
            # Generate a unique token for the user
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Get the host from the request
            current_host = HttpRequest.get_host(request)
            reset_url = f"{request.scheme}://{current_host}{reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})}"
            
            # Email content
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
            sender_email = 'ptms2525@gmail.com'  # Your email
            send_mail(subject, message, sender_email, [user.email])

            messages.success(request, 'A password reset link has been sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'No account found with that username or email. Please register.')
            return render(request, self.template_name)

from django.contrib.auth.hashers import make_password

class PasswordResetConfirmView(View):
    template_name = 'password_reset_confirm.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, self.template_name, {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('login')

    def post(self, request, uidb64, token, *args, **kwargs):
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if new_password != confirm_new_password:
            messages.error(request, "Passwords do not match.")
            return redirect('password_reset_confirm', uidb64=uidb64, token=token)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Reset the user's password
            hashed_password=make_password(new_password)
            user.password=hashed_password
            user.save()
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('login')
        else:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('login')
