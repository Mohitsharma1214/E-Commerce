from django.shortcuts import render
from django.views import View

class RefundPolicyView(View):
    def get(self, request):
       
        return render(request, 'refund_policy.html')
    
from django.shortcuts import render
from django.views import View

class PrivacyPolicyView(View):
    def get(self, request):
       
        return render(request, 'privacy_policy.html')    

class termsandserviceView(View):
    def get(self,request):
        return render(request,'termsofservice_policy.html')        
    
class ShippingPolicyView(View):
    def get(self,request):
        return render(request,'shipping_policy.html')    

class ContactInfoView(View):
    def get(self,request):
        return render(request,'contact_info.html')              