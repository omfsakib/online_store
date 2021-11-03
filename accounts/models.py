from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null = True,blank=True ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True )
    profile_pic = models.ImageField(default="profile.png",null = True,blank = True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

class ShopOwner(models.Model):
    user = models.OneToOneField(User, null = True,blank=True ,on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True )
    profile_pic = models.ImageField(default="profile.png",null = True,blank = True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        print('Profile created')


def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.UserProfile.save()
        print('Profile Updated')


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.ManyToManyField(Category)
    description = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    digital = models.BooleanField(default=False, null=True, blank=False)
    img = models.ImageField(default="product-pic.jpg",null = True,blank = True)
    stock = models.IntegerField(default=0, null = True,blank = True)
    discount = models.IntegerField(default=0, null = True,blank = True)
    discount_amount = models.FloatField(default=0, null = True,blank = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    



