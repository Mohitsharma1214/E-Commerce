from django.db import models
from datetime import date

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

    def is_expired(self):
        return self.expiry_date < date.today()
