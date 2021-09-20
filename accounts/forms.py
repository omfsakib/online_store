from django.forms import ModelForm, fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields ='__all__'
        exclude = ['user']

class ShopOwnerForm(ModelForm):
    class Meta:
        model = ShopOwner
        fields ='__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class UpdateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields =['email','first_name','last_name','password']