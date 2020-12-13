from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, CustomerForm, RecordForm, Indi_CustForm, Corp_custForm,VehicleForm
from .models import Rental_Record, Customer, Indi_cust, Corp_cust, \
     Veh_class, Vehicle, Invoice, Payment, Location, Corporation, Coupon
from django.contrib import auth
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('/cust_details/'+str(customer.customer_id))
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    return render(request, 'register.html', 
        {'user_form':user_form, 'customer_form':customer_form})

def cust_details(request, id):
    registered = False
    indi = True
    customer = Customer.objects.get(customer_id=id)
    corporations = Corporation.objects.all()
    if customer.cust_type == 'I':
        form = Indi_CustForm()
    else:
        indi = False
        form = Corp_custForm()
    if request.method == "POST":
        if customer.cust_type == 'I':
            form = Indi_CustForm(request.POST)
        else:
            form = Corp_custForm(request.POST)
        if form.is_valid():
            cust = form.save(commit=False)
            cust.customer = customer
            cust.save()
            registered = True
    return render(request, 'cust_details.html', {'form':form, 
        'registered':registered, 'indi':indi, 'corporations':corporations})
    

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
            path = request.GET.get("next") or "/index"
            return redirect(path)
        else:
            return redirect('/accounts/login/')
    return render(request, 'login.html')

def reset_password(request):
    reset = False
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            new_password = request.POST.get("password")
            user.set_password(new_password)
            user.save()
            reset = True
        except:
            form.add_error('username',"Username doesn't exist!")
    else:
        form = UserForm()
    return render(request, 'reset_password.html', {'form':form, 'reset':reset})

@login_required
def profile(request):
    info = Customer.objects.get(user=request.user)
    indi = True
    if info.cust_type == 'I':
        details = Indi_cust.objects.get(customer=info)
    else:
        indi = False
        details = Corp_cust.objects.get(customer=info)
    return render(request, 'profile.html', 
        {'info':info, 'details':details, 'indi':indi})

@login_required
def edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    cust_form = CustomerForm(request.POST, instance=customer)
    corporations = Corporation.objects.all()
    indi = True
    if customer.cust_type == 'I':
        detail = Indi_cust.objects.get(customer=customer)
        detail_form = Indi_CustForm(request.POST, instance=detail)
    else:
        indi = False
        detail = Corp_cust.objects.get(customer=customer)
        detail_form = Corp_custForm(request.POST, instance=detail)
    if cust_form.is_valid() and detail_form.is_valid():
        cust = cust_form.save(commit=False)
        cust.user = request.user
        cust.save()
        detail = detail_form.save(commit=False)
        detail.customer = cust
        detail.save()
        return redirect('/info')
    return render(request, 'edit_profile.html', {'cust_form':cust_form, 'detail_form':detail_form, 
        'customer':customer, 'detail':detail, 'indi':indi, 'corporations':corporations})

@login_required
def record_add(request):
    # employee auth
    customers = Customer.objects.all()
    vehicles = Vehicle.objects.all()
    locations = Location.objects.all()
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            try:
                record = form.save(commit=False)
                customer = record.customer
                record.user = customer.user
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = RecordForm()
    return render(request, 'record_add.html', {'form': form, 
        'customers':customers, 'vehicles':vehicles, 'locations':locations})

@login_required
def record_show(request):
    if request.user.is_superuser:
        records = Rental_Record.objects.all()
    else:
        records = Rental_Record.objects.filter(user=request.user)
    return render(request, 'record_show.html', {'records':records})


@login_required
def record_update(request, id):
    # employee auth
    customers = Customer.objects.all()
    vehicles = Vehicle.objects.all()
    locations = Location.objects.all()
    record = Rental_Record.objects.get(record_id=id)
    if request.method == "POST":
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = record.customer.user
            form.save()
            return redirect("/show")
    else:
        form = RecordForm()
    return render(request, 'record_edit.html', {'form': form, 'record':record,
        'customers':customers, 'vehicles':vehicles, 'locations':locations})

@login_required
def record_destroy(request, id):
    # employee auth
    record = Rental_Record.objects.get(record_id=id)
    record.delete()
    return redirect("/show")

@login_required
def vehicle_add(request):
    classes = Veh_class.objects.all()
    locations = Location.objects.all()
    if request.method =="POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vehi_show')
    else:
        form = VehicleForm()
    return render(request, 'vehicle_add.html',{'form':form,
        'classes':classes, 'locations':locations})

@login_required
def vehicle_show(request):
    records = Vehicle.objects.all()
    return render(request, 'vehicle_show.html', {'records':records})

@login_required
def vehicle_update(request, id):
    # employee auth
    classes = Veh_class.objects.all()
    locations = Location.objects.all()
    vehicle = Vehicle.objects.get(vehicle_id=id)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect("/vehi_show")
    else:
        form = VehicleForm()
    return render(request, 'vehicle_edit.html', {'form':form,
        'vehicle':vehicle, 'classes':classes, 'locations':locations})

@login_required
def vehicle_destroy(request, id):
    # employee auth
    vehicle = Vehicle.objects.get(vehicle_id=id)
    vehicle.delete()
    return redirect("/vehi_show")

def indi_cust_coupon(request):
    indi_custs = Indi_cust.objects.all()
    coupons = Coupon.objects.all()
    for indi in indi_custs:
        indi.coupon.add(*coupons)
    return render(request, 'index.html')

@login_required
def gene_invoice(request, id):
    record = Rental_Record.objects.get(record_id=id)
    try:
        invoice = Invoice.objects.get(record=record)
    except:
        idate = timezone.localtime()
        vehicle = record.vehicle
        veh_class = vehicle.class_id
        rent_duration = (record.dropoff_date - record.pickup_date).days
        overfee = 0
        if record.odo_limit:
            total_odo = record.end_odo - record.start_odo
            if total_odo > rent_duration * record.odo_limit:
                overfee = veh_class.fees * \
                    (total_odo - rent_duration * record.odo_limit)
        amount = rent_duration * veh_class.rental_rate + overfee
        invoice = Invoice.objects.create(idate=idate, amount=amount, record=record)
    
    # corportaion discount
    indi = True
    customer = record.customer
    if customer.cust_type == 'C':
        indi = False
        detail = Corp_cust.objects.get(customer=customer)
        discount = detail.corp.corp_discount
    else:
        detail = Indi_cust.objects.get(customer=customer)
    # create payment and redirect to payment page
    if request.method == "POST":
        method = request.POST.get("method")
        card_num = request.POST.get("card_num")
        pdate = timezone.localtime()
        #customer = record.customer
        if customer.cust_type == 'I':
            if request.POST.get("coupon"):
                coupon_id = request.POST.get("coupon")
                coupon = Coupon.objects.get(coupon_id=coupon_id)
                discount = coupon.discount
                # delete this coupon after used
                detail.coupon.remove(coupon)
            else:
                discount = 0.00
        payment = Payment.objects.create(customer=customer, pdate=pdate,
            method=method, card_num=card_num, invoice=invoice, discount=discount)
        # after payment, we will change the payment 
        # status of this record to paid 
        record.payment = True
        record.save()
        return redirect('/payment/'+str(record.record_id))

    return render(request, 'invoice.html', {'invoice': invoice,
        'indi':indi, 'detail':detail})

@login_required
def payment(request, id):
    record = Rental_Record.objects.get(record_id=id)
    invoice = Invoice.objects.get(record=record)
    payment = Payment.objects.get(invoice=invoice)
    discounted_amount = invoice.amount*(1-payment.discount)
    return render(request, 'payment.html', 
        {'payment':payment, 'discounted_amount':discounted_amount})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')

