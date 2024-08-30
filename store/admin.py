from django.contrib import admin
from .models.product import Products, Size
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.coupon import Coupon

from django.contrib import admin
from .models.orders import Order
from .models.product import Products
from .models.tags import Tag
from django.contrib import admin
from .models.address import Address
from .models.newsletter import Newsletter
from .models.subsrciber import Subscriber
from .models.contact import ContactMessage
from .models.customerrating import Review

class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class for other model admin classes.
    """
    list_per_page = 20  # Number of items per page in the admin list view
    actions_on_top = True  # Display actions at the top of the admin change list
    actions_on_bottom = False  # Display actions at the bottom of the admin change list
    date_hierarchy = None  # Date hierarchy navigation (e.g., by year, month, and day)

    def get_queryset(self, request):
        """
        Override the queryset method to customize the queryset for the admin list view.
        """
        qs = super().get_queryset(request)
        # Add custom queryset filtering or annotation here if needed
        return qs

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to perform additional actions when saving an object in the admin interface.
        """
        super().save_model(request, obj, form, change)
        # Add custom save actions here if needed

    def delete_model(self, request, obj):
        """
        Override the delete_model method to perform additional actions when deleting an object in the admin interface.
        """
        super().delete_model(request, obj)
        # Add custom delete actions here if needed

    # Add more common configurations or custom methods as needed


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price', 'status']
    list_filter = ['status']
    search_fields = ['product__name', 'customer__name']



admin.site.register(Products, ProductAdmin)
admin.site.register(Category, BaseAdmin)
admin.site.register(Customer, BaseAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, BaseAdmin)
admin.site.register(Tag,BaseAdmin)
admin.site.register(Address,BaseAdmin)
admin.site.register(Subscriber,BaseAdmin)
admin.site.register(Newsletter,BaseAdmin)
admin.site.register(ContactMessage,BaseAdmin)
admin.site.register(Review,BaseAdmin)
admin.site.register(Size,BaseAdmin)