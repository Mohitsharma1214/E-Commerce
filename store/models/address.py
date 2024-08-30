from django.db import models
from .product import Products
from .customer import Customer
import datetime
# Assuming your Address model looks something like this:
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Address for {self.customer}: {self.address}"
