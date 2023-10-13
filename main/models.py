from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE, ManyToManyField, BooleanField


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    color = models.CharField(max_length=75)

    def __str__(self):
        return self.color


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    description = models.TextField()
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    released_on = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255, null=True)
    display_size = models.CharField(max_length=255, null=True)
    to_category = ManyToManyField(Category, related_name='categories')
    to_color = ManyToManyField(ProductColor, related_name='colors')
    is_active = BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    to_product = models.ForeignKey(Product, CASCADE)


class ProductShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField()
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    sum_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.sum_price = self.count * self.product.price
        self.price = self.product.price
        return super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=128)
    submit = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
