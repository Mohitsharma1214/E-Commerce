from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from store.models.category import Category
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password

class Signup(View):
    return_url = None
    def get(self, request):
        categories = Category.get_all_categories()
        return render(request, 'signup.html', {'categories': categories})

    def post(self, request):
        postData = request.POST
        
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email').lower()
        username = postData.get('username')
        password = postData.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'username': username
        }
        error_message = self.validateCustomer(first_name, last_name, phone, email, username, password)

        if not error_message:
            # Create and save the customer
            customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                username=username,
                                password=make_password(password))
            customer.save()

            # Manually log in the user by setting session key
            
            if customer:
                flag = check_password(password, customer.password)
                if flag:
                    request.session['customer'] = customer.id

                    if Signup.return_url:
                        return HttpResponseRedirect(Signup.return_url)
                    else:
                        Signup.return_url = None
                        return redirect('homepage')
                
                else:
                    error_message = 'Invalid !!'
            else:
                error_message = 'Invalid !!'
                return redirect('homepage')
        
        # If there's an error, render the signup page again with the error message
        data = {'error': error_message, 'values': value}
        return render(request, 'signup.html', data)
        
    def validateCustomer(self, first_name, last_name, phone, email, username, password):
        error_message = None
        if not first_name:
            error_message = "Please enter your First Name!"
        elif len(first_name) < 3:
            error_message = 'First Name must be at least 3 characters long'
        elif not last_name:
            error_message = 'Please enter your Last Name!'
        elif len(last_name) < 3:
            error_message = 'Last Name must be at least 3 characters long'
        elif not phone:
            error_message = 'Please enter your Phone Number!'
        elif len(phone) != 10:
            error_message = 'Phone Number must be 10 characters long'
        elif not username:
            error_message = 'Please enter your Username!'
        elif len(username) < 5:
            error_message = 'Username must be at least 5 characters long'
        elif not password:
            error_message = 'Please enter your Password!'
        elif len(password) < 5:
            error_message = 'Password must be at least 5 characters long'
        elif not email:
            error_message = 'Please enter your Email!'
        elif len(email) < 5:
            error_message = 'Email must be at least 5 characters long'
        elif Customer.objects.filter(username=username).exists():
            error_message = 'Username is already taken, please choose another one!'
        elif Customer.objects.filter(email=email).exists():
            error_message = 'The account with this email already exists, please signup with another email!'    

        return error_message
