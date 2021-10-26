from django.shortcuts import render
from accounts.models import *
from .filters import ProductFilter

# Create your views here.
def store(request):
    products = Product.objects.all()
    productFilter = ProductFilter(request.GET,queryset=products)
    products = productFilter.qs
    context = {'products':products,'productFilter':productFilter}
    return render(request, 'store/store.html',context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html',context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html',context)