from django.forms import ModelForm, fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from ecommerce_web.models import *

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
        model = OrderItem
        fields = '__all__'

class UpdateOrderForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['customer']

class ProductForm(ModelForm):
    name = forms.CharField(label='Product Name',widget=forms.TextInput(attrs={'placeholder': 'Product Name'}))
    price = forms.FloatField(label='Price',widget=forms.TextInput(attrs={'placeholder': 'Price'}))
    description = forms.CharField(max_length=50,label='Description',widget=forms.Textarea(attrs={'placeholder': 'Max 50 words'}))
    tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)
    category = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True)
    
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