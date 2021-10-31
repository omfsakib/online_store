from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django_pandas.io import read_frame
from .models import *
from ecommerce_web.models import *
from .forms import *
from ecommerce_web.forms import *
from django.contrib.auth import authenticate,login,logout
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticted_user, allowed_users,shopowner_only

# Create your views here.

@unauthenticted_user
def registerPage(request):
    form = CreateUserForm()
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            elif User.objects.filter(email=email).first():
                messages.success(request, 'This Email is taken.')
                return redirect('/register')

            if form.is_valid():
                user_obj = User.objects.create(username =username,email=email)
                user_obj.set_password(password)
                user_obj.save()
                auth_token=str(uuid.uuid4())
                profile_obj = UserProfile.objects.create(user = user_obj,auth_token=auth_token)
                profile_obj.save()
                group = Group.objects.get(name = 'customer')
                user_obj.groups.add(group)
                Customer.objects.create(
                    user = user_obj
                )
                send_mail_after_registration(email,auth_token)
                messages.success(request,'Account was created for ' + username)
                return redirect('/token')
        
        except Exception as e:
            print(e)

    context = {'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticted_user
def shopOwnerRegisterPage(request):
    form = CreateUserForm()
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/shopregister')

            elif User.objects.filter(email=email).first():
                messages.success(request, 'This Email is taken.')
                return redirect('/shopregister')

            if form.is_valid():
                user_obj = User.objects.create(username =username,email=email,is_staff = True)
                user_obj.set_password(password)
                user_obj.save()
                auth_token=str(uuid.uuid4())
                profile_obj = UserProfile.objects.create(user = user_obj,auth_token=auth_token)
                profile_obj.save()
                group = Group.objects.get(name = 'shopowner')
                user_obj.groups.add(group)
                ShopOwner.objects.create(
                    user = user_obj
                )
                send_mail_after_registration(email,auth_token)
                messages.success(request,'Account was created for ' + username)
                return redirect('/token')
        
        except Exception as e:
            print(e)

    context = {'form':form}
    return render(request,'accounts/shopregister.html',context)

def success(request):
    return render(request, 'accounts/success.html')

def token_send(request):
    return render(request, 'accounts/token_send.html')

def send_mail_after_registration(email,token):
    subject = 'Account activation for Online Store'
    message = f'Hello there! Click this link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_form,recipient_list)

def verify(request,auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    
    except Exception as e:
        print(e)

def error_page(request):
    return render(request,'accounts/error.html')

@unauthenticted_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is incorrect')
    context = {}
    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@shopowner_only
def home(request):
    orders = OrderItem.objects.all().order_by('-date_added')
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders,'customers':customers,
    'total_customers':total_customers,'total_orders':total_orders,
    'delivered':delivered,'pending':pending
    }

    return render(request,'accounts/dashboard.html', context)

@login_required(login_url='login')
def userPage(request):
    orders = request.user.customer.orderitem_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {'orders':orders,'total_orders':total_orders,
    'delivered':delivered,'pending':pending,'myFilter':myFilter}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
def viewAccount(request, pk = None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user':user}
    return render(request,'accounts/account.html',args)

@login_required(login_url='login')
def accountSettings(request):
    group = Group.objects.get(name = 'customer')
    print(group)
    try: 
        customer = request.user.customer
        form = CustomerForm(instance=customer)
    except:
        shopowner = request.user.shopowner
        form = ShopOwnerForm(instance=shopowner)
    form2 = UpdateProfileForm(instance=request.user)
    if request.method == 'POST':
        try:
            form = CustomerForm(request.POST, request.FILES, instance=customer)
        except:
            form = ShopOwnerForm(request.POST, request.FILES, instance=shopowner)
        form2 = UpdateProfileForm(request.POST, instance=request.user)
        if (form and form2).is_valid():
            form.save()
            form2.save()
            return redirect('/account')
    context = {'form':form,'form2':form2}
    return render(request,'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['shopowner'])
def products(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    products = Product.objects.all()

    context ={'products':products,'form':form}
    return render(request,'accounts/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['shopowner'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.orderitem_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createorder(request,pk):
    OrderFormSet =inlineformset_factory(Customer, Order, fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet()
    #form = OrderForm(initial={'customer':customer})
    if request.method =='POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['shopowner'])
def updateOrder(request,pk):
    order = OrderItem.objects.get(id=pk)
    form = UpdateOrderForm(instance=order)
    if request.method =='POST':
        form = UpdateOrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form,'order':order}
    return render(request,'accounts/update_order.html',context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = OrderItem.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['shopowner'])
def mail_letter(request):
    emails = Subscriber.objects.all()
    df = read_frame(emails, fieldnames=['email'])
    mail_list = df['email'].values.tolist()
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            send_mail(
                title,
                message,
                '',
                mail_list,
                fail_silently=False
            )
            messages.success(request, 'Message has sent to all Subscribers')
            return redirect('/mail')
    else:
        form = MailMessageForm()
    
    mails = MailMessage.objects.all().order_by('-id')

    context = {'form':form,'mails':mails,'emails':emails}
    return render(request, 'accounts\mail_letter.html',context)
