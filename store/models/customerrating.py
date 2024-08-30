from django.db import models
from django.utils import timezone

from store.models.customer import Customer
from .product import Products

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)  # Allow null values for the customer
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(default=timezone.now)  # Provide a default value for review_date

    def __str__(self):
        return f"Review for {self.product.name} - Rating: {self.rating}"
