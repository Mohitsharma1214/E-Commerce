from django.contrib import admin
from django.urls import path

from store.views.search import SearchView
from store.views.submitreview import  submit_review
from store.views.subscriber import send_newsletter, subscribe
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart, cart_count
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.coupon import ApplyCoupon, RemoveCoupon
from .middlewares.auth import  auth_middleware
from .views.remove import RemoveFromCart
from .views.product import ProductDetailView
from .views.increase import increase as Increase
from .views.profile import CustomerProfileEditView,CustomerProfileView
from .views.password import PasswordResetRequestView, PasswordResetConfirmView
from django.utils.encoding import force_str
from store.views.policies import RefundPolicyView,PrivacyPolicyView,termsandserviceView,ShippingPolicyView,ContactInfoView
from store.views.contact import contact


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
     path('customer/profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('customer/profile/edit/', CustomerProfileEditView.as_view(), name='customer_profile_edit'),
     path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('apply-coupon', ApplyCoupon.as_view(), name='apply_coupon'),
    path('remove-coupon', RemoveCoupon.as_view(), name='remove_coupon'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('cart/count/', cart_count, name='cart_count'),
    path('remove-cart', RemoveFromCart.as_view(), name='remove_cart'),
    path('increase-cart', Increase.as_view(), name='increase-cart'),
    path('product-detail/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', SearchView, name='search'), 
    path('submit_review/', submit_review, name='submit_review'),
    
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('subscribe/', subscribe, name='subscribe'),
    path('send-newsletter/', send_newsletter, name='send_newsletter'),
    path('policies/refund-policy', RefundPolicyView.as_view(), name='refund_policy'),
    path('policies/privacy-policy', PrivacyPolicyView.as_view(), name='refund_policy'),
    path('policies/termsofservice',termsandserviceView.as_view(),name='terms_service'),
    path('policies/shipping-policy',ShippingPolicyView.as_view(),name='shipping_policy'),
    path('policies/contact-info',ContactInfoView.as_view(),name='contact_info'),
    path('contact/',contact,name='contact')
    
]
 
