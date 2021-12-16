from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class  Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="bgImage.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def  __str__(self):
        return self.name

class  Tags(models.Model):
    name = models.CharField(max_length=200, null=True)

    def  __str__(self):
        return self.name

class Product(models.Model):
    CATEGOTY=(
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door')
    )
    name = models.CharField(max_length= 200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length= 200, null=True, choices=CATEGOTY)
    description = models.CharField(max_length= 200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tags)

    def  __str__(self):
        return self.name

class Order(models.Model):
    STATUS= (
        ('Pending', 'pending'),
        ('Out of delivery','Out of delivery'),
        ('Delivered','Delivered')
        )
    Customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    Product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    def  __str__(self):
        return self.Product.name
        #return str(self.Customer.name) 