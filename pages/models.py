from django.db import models
from django.contrib.auth.models import User


# Create your models here.

from django.db import models


#### product code 
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Mobile', 'Mobile'),
        ('PC', 'PC'),
        ('Tablet', 'Tablet'),
        ('Camera', 'Camera'),
        ('Smartwatch', 'Smartwatch'),
        # Add more categories as needed
    ]

    gadgetName = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Choose category
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    gadgetImage = models.ImageField(upload_to='gadgets/images/')  # Update upload_to path
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gadgetName


#### profile code 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='media/profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    

#### cart code

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.price
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.locality}, {self.city}, {self.state} - {self.zipcode}"

STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    Payment= models.ForeignKey(Payment, on_delete=models.CASCADE,default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.price




    


    




    
    