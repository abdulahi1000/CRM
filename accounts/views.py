from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate,login,logout

from .models import *
from .forms import *
from .filters import orderFilter
from .decorators import unauthenticated_user, allowed_user, admin_only


# Create your views here.
@unauthenticated_user
def register(request):  

    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

           # group = Group.objects.get(name='customer')
           # user.groups.add(group)
           # Customer.objects.create(
           #     user=user,
           # )
            
            messages.success(request, 'Account was created for '+username )
            return redirect('login')
    context={
        'form': form
    
    }
    return render(request, 'accounts/register.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incoorect')

    context={
    }
    return render(request, 'accounts/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context={
        'customers': customers ,
        'orders': orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending': pending,
       
    }
    return render(request, 'accounts/dashboard.html', context)
@login_required(login_url='login')
@allowed_user(allowed_roles =['customer'])
def userPage(request):
    orders =request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context={
       'orders':orders,
       'total_orders':total_orders,
        'delivered':delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)
@login_required(login_url='login')
@allowed_user(allowed_roles =['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = customerForm(instance=customer)
    if request.method == 'POST':
        form = customerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()


    context={
        'form':form
    }
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles =['admin'])
def product(request):
    products = Product.objects.all()
    context={
        'products': products 
       
    }

    return render(request, 'accounts/products.html', context)
@login_required(login_url='login')
@allowed_user(allowed_roles =['admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    orders_count = orders.count()

    myfilter = orderFilter(request.GET, queryset=orders)
    orders= myfilter.qs 

    context={
        'customers':customers,
        'orders':orders,
        'orders_count':orders_count,
        'myfilter': myfilter
       
    }
    return render(request, 'accounts/customer.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles =['admin'])
def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('Product', 'status'), extra=5) 
    customers = Customer.objects.get(id=pk)
    
    formSet = orderFormSet(queryset=Order.objects.none() , instance=customers)
    #form = orderForm(initial={'Customer': customers})
    if request.method == 'POST':
       # form = orderForm(request.POST)
        formSet = orderFormSet(request.POST, instance=customers)
        if formSet.is_valid():
            formSet.save()
            return redirect('/')

    context={
        'formSet': formSet,
        'customers':customers,
       
    }
    return render(request, 'accounts/order_form.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles =['admin'])
def updateOrder(request, pk):
    orders = Order.objects.get(id=pk)
    form = orderForm(instance=orders)
    if request.method == 'POST':

        form = orderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={
        'orders':orders,
        'forms': form,
       
    }
    return render(request, 'accounts/order_form.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles =['admin'])
def deleteOrder(request, pk):
    orders = Order.objects.get(id=pk)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')
    context={
        'orders':orders,
       
    }
    return render(request, 'accounts/delete.html',context)

