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

class Product(models.Model):
    CATEGORY =(
        ('Indoor','Indoor'),
        ('Out Door','Out Door')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True,choices=CATEGORY)
    description = models.CharField(max_length=200, null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered','Delivered')
    ) 
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True,choices=STATUS)

    def __str__(self):
        return self.product.name    
    



