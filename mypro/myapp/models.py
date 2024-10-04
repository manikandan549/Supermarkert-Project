from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    User_id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    designation = models.CharField(max_length=20, choices=[('Manager', 'Manager'), ('Sales Man', 'Sales Man')],default="")
    username=None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100,unique=True)
    rate = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.product_name


class Purchase(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases',to_field='product_name')
    quantity = models.IntegerField()
    amount = models.IntegerField()
    date_of_purchase = models.DateField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new purchase (not updating an existing one)
            product_rate = self.product_name.rate
            self.amount = self.product_name.rate * self.quantity
        super().save(*args, **kwargs)

