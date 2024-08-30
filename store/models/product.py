from django.db import models
from .category import Category
from .tags import Tag
from django.db.models import Count
from datetime import datetime, timedelta

from django.db import models

from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

from django.db import models
from .category import Category
from .tags import Tag
from django.db.models import Count
from datetime import datetime, timedelta

class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    deleted_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=10000, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')
    created_at = models.DateTimeField(default=datetime.now)
    tags = models.ManyToManyField(Tag, blank=True)  # Allow multiple tags
    sizes = models.ManyToManyField(Size, blank=True)  # Allow multiple sizes

    def get_related_products(self):
        related_by_category = (
            Products.objects.filter(category=self.category).exclude(pk=self.pk)
            .annotate(category_count=Count('category'))
            .order_by('-category_count')[:5]
        )

        related_by_tags = (
            Products.objects.filter(tags__in=self.tags.all()).exclude(pk=self.pk)
            .annotate(tag_count=Count('tags', distinct=True))
            .order_by('-tag_count')[:5]
        )

        related_products = list(set(related_by_category) | set(related_by_tags))

        for product in related_products:
            product.deleted_price = product.price + 50

        return related_products

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()

    @staticmethod
    def get_new_drops():
        seven_days_ago = datetime.now() - timedelta(days=7)
        new_drops = Products.objects.filter(created_at__gte=seven_days_ago)

        for product in new_drops:
            product.deleted_price = product.price + 50

        return new_drops

    @staticmethod
    def get_recently_viewed_products(request):
        viewed_product_ids = request.session.get('viewed_product_ids', [])
        viewed_products = Products.objects.filter(id__in=viewed_product_ids)

        return viewed_products
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Call the superclass's save method to perform the actual saving
        super().save(*args, **kwargs)
        # Automatically add all available sizes upon creation
        if not self.sizes.exists():
            all_sizes = Size.objects.all()
            self.sizes.set(all_sizes)
