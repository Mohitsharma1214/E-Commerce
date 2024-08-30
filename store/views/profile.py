from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.category import Category
from store.models.customer import Customer
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
  # Import the Category model

class CustomerProfileView(DetailView):
    model = Customer
    template_name = 'customer_profile.html'
    context_object_name = 'customer'

    def get_object(self, queryset=None):
        customer_id = self.request.session.get('customer')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            return customer
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.request.session.get('customer')
        if customer_id:
            addresses = Address.objects.filter(customer_id=customer_id)
            categories = Category.objects.all()  # Fetch all categories
            context['addresses'] = addresses
            context['categories'] = categories  # Pass categories to the context
        return context

        
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address  # Import Address model

from django.shortcuts import redirect
from django.views.generic import UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.shortcuts import redirect
from django.views.generic import UpdateView
from store.models.customer import Customer
from store.models.address import Address
from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address  # Import the Address model

from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.shortcuts import redirect
from django.views.generic import UpdateView
from store.models.customer import Customer
from store.models.address import Address
from django.contrib.auth.hashers import make_password  # Import make_password

from django.contrib.auth.hashers import check_password, make_password

from django.contrib.auth.hashers import check_password, make_password

from django.contrib import messages

from django.contrib.auth.hashers import check_password

from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.views.generic import UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.views.generic import UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.views.generic import UpdateView
from store.models.customer import Customer
from store.models.address import Address

from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash  # Import update_session_auth_hash

from django.shortcuts import redirect
from django.views.generic import DetailView, UpdateView
from store.models.customer import Customer
from store.models.address import Address


from django.contrib.auth.hashers import check_password




from django.contrib.auth.hashers import check_password

from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import UpdateView


class CustomerProfileEditView(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'phone', 'email']
    template_name = 'customer_profile_edit.html'
    success_url = '/customer/profile/'

    def get_object(self, queryset=None):
        customer_id = self.request.session.get('customer')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            return customer
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.request.session.get('customer')
        if customer_id:
            addresses = Address.objects.filter(customer_id=customer_id)
            categories = Category.objects.all()  # Fetch all categories
            
            context['categories'] = categories 
            context['addresses'] = addresses
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        
        if action == 'add_address':
            new_address = self.request.POST.get('new_address')
            if new_address:
                customer_id = self.request.session.get('customer')
                if customer_id:
                    customer = Customer.objects.get(id=customer_id)
                    
                    address = Address.objects.create(customer=customer, address=new_address)
                    form.instance.address = address
                    return redirect('customer_profile_edit')
            else:
                messages.error(self.request,'Please fill the address to update the new address')
                return redirect('customer_profile_edit')
        elif action == 'save_changes':
            address_id = self.request.POST.get('address')
            if address_id:
                address = Address.objects.get(id=address_id)
                form.instance.address = address
        
        elif action == 'update_password':
            current_password = self.request.POST.get('current_password')
            new_password = self.request.POST.get('new_password')
            if not current_password:
                messages.error(self.request, 'Please provide your current password.')
                return redirect('customer_profile_edit')
            elif not new_password:
                messages.error(self.request, 'Please provide a new password.')
                return redirect('customer_profile_edit')
            else:
                self.update_password(form)
                return redirect('customer_profile_edit')

        return super().form_valid(form)

    def update_password(self, form):
        
            current_password = self.request.POST.get('current_password')
            new_password = self.request.POST.get('new_password')
            customer = self.get_object()
            if check_password(current_password, customer.password):
                # Update the password
                hashed_pass=make_password(new_password)
                customer.password=hashed_pass
                customer.save()
                
                # Add success message
                messages.success(self.request, 'Password updated successfully.')
                return redirect('customer_profile_edit')
            else:
                # If the current password is incorrect, add an error message
                messages.error(self.request, 'Incorrect current password')
                return redirect('customer_profile_edit')