from django.db import models

from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, default='default_username')  
    phone = models.CharField(max_length=10)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address = models.OneToOneField('Address', on_delete=models.SET_NULL, null=True, blank=True, related_name='profile')

    def save(self, *args, **kwargs):
        if not self.username:  
            self.username = f'{self.first_name}_{self.last_name}'
        super().save(*args, **kwargs)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def isExists(self):
        return Customer.objects.filter(email=self.email).exists()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
