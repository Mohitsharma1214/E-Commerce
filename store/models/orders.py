from django.db import models
from .product import Products, Size
from .customer import Customer
from .address import Address
from datetime import datetime, timedelta

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped','Shipped'),
        ('Out for Delievery','Out for Delievery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20, default='0')  # Updated phone field
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)  # Add size field
    price = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, default='', blank=True)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-created_at')

    def __str__(self):
        return f"PRODUCT: {self.product.name}, CUSTOMER: {self.customer.first_name} , QUANTITY: {self.quantity}, SIZE: {self.size}, PRICE: {self.price}, STATUS: {self.status}"
