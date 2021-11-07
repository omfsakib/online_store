from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.http import JsonResponse
from accounts.models import *
from .filters import ProductFilter
import json
import datetime
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_users
from .forms import SubscribeForm,ReviewForm

# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def store(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription Successful')
            return redirect('/store')
    else:
        form = SubscribeForm()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    products = Product.objects.all().order_by('-date_created')
    date = timezone.now().date() - timedelta(days=7)
    product_week = Product.objects.filter(date_created__gt=(datetime.datetime.now()- timedelta(days=7))).order_by('-date_created')
    shops = ShopOwner.objects.all().count()
    customers = Customer.objects.all().count()
    subscribers = Subscriber.objects.all()
    total_subscriber = subscribers.count()
    total_products = products.count()
    productFilter = ProductFilter(request.GET,queryset=products)
    top_reviewed = Review.objects.all().order_by('rate')
    products = productFilter.qs
    context = {
    'total_products':total_products,
    'top_reviewed':top_reviewed,
    'product_week':product_week,
    'customers':customers,
    'shops':shops,
    'total_subscriber':total_subscriber,
    'form':form,
    'products':products,
    'cartItems':cartItems,
    'productFilter':productFilter
    }
    return render(request, 'store/store.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
    shops = ShopOwner.objects.all().count()
    customers = Customer.objects.all().count()
    subscribers = Subscriber.objects.all()
    total_subscriber = subscribers.count()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
    context = {'customers':customers,'shops':shops,'total_subscriber':total_subscriber,'items':items,'cartItems':cartItems,'order':order}
    return render(request, 'store/cart.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
    shops = ShopOwner.objects.all().count()
    customers = Customer.objects.all().count()
    subscribers = Subscriber.objects.all()
    total_subscriber = subscribers.count()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
    context = {'customers':customers,'shops':shops,'total_subscriber':total_subscriber,'items':items,'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(customer=customer, order=order, product=product, status='Pending')

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('User is not logged in...')
    return JsonResponse('Payment complete!', safe=False)

def productView(request,pk):
    shops = ShopOwner.objects.all().count()
    customers = Customer.objects.all().count()
    subscribers = Subscriber.objects.all()
    total_subscriber = subscribers.count()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
    product = Product.objects.get(id = pk)
    demo_price = product.price + product.discount_amount

    review = product.review_set.all()
    total_review = review.count()
    total_rate = 0
    for i in review:
        total_rate += i.rate
    try:
        avg_rating = total_rate/total_review
    except:
        avg_rating = 0
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        form.save()
        messages.success(request, 'Review Added')
        return redirect(reverse('view', kwargs={'pk':pk}))
    
    else:
        form = ReviewForm()

    stock = product.stock
    context = {'demo_price':demo_price,'stock':stock,'avg_rating':avg_rating,'review':review,'total_review':total_review,'form':form,'product':product,'customers':customers,'shops':shops,'total_subscriber':total_subscriber,'cartItems':cartItems}
    return render(request, "store/view.html",context)

@login_required(login_url='login')
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == "POST":
        review.delete()
        return redirect('/')

    context = {'item':review}
    return render(request,'store/delete.html',context)