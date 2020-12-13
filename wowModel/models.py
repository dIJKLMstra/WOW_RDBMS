from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Veh_class(models.Model):
    class_id = models.DecimalField(max_digits=4,decimal_places=0,primary_key=True)
    class_name = models.CharField(max_length=32)
    rental_rate = models.DecimalField(max_digits=10,decimal_places=2)
    fees = models.DecimalField(max_digits=10,decimal_places=2)
    class Meta:  
        db_table = "class"  

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=50)
    zipcode = models.DecimalField(max_digits=5,decimal_places=0)
    phone = models.DecimalField(max_digits=11, decimal_places=0)
    class Meta:  
        db_table = "location"  

class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    year = models.DecimalField(max_digits=4,decimal_places=0)
    vin = models.CharField(max_length=17)
    lp_num = models.CharField(max_length=10)
    class_id = models.ForeignKey(Veh_class, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    class Meta:  
        db_table = "vehicle"  

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=32)
    lname = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    street = models.CharField(max_length=50)
    zipcode = models.DecimalField(max_digits=5,decimal_places=0)
    email = models.EmailField()     
    phone = models.DecimalField(max_digits=11, decimal_places=0)
    cust_type = models.CharField(max_length=1)
    class Meta:  
        db_table = "customer"  

class Rental_Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pickup_date =  models.DateField()
    dropoff_date = models.DateField()
    start_odo = models.DecimalField(max_digits=10,decimal_places=0)
    end_odo = models.DecimalField(max_digits=10,decimal_places=0)
    odo_limit = models.DecimalField(max_digits=10,decimal_places=0,null=True, blank=True)
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE)
    pu_location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name='pu_location_id')
    do_location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name='do_location_id')
    payment = models.BooleanField(default=False)
    class Meta:  
        db_table = "rental_record"  

class Coupon(models.Model):
    coupon_id = models.DecimalField(max_digits=4,decimal_places=0,primary_key=True)
    discount = models.DecimalField(max_digits=4,decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:  
        db_table = "coupon"  

class Corporation(models.Model):
    corp_id = models.AutoField(primary_key=True)
    corp_name = models.CharField(max_length=32)
    corp_reg_num = models.CharField(max_length=20)
    corp_discount = models.DecimalField(max_digits=3,decimal_places=2)
    class Meta:  
        db_table = "corporation"  

class Indi_cust(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    dl_num = models.CharField(max_length=15)
    insur_com_name = models.CharField(max_length=32)
    insur_polic_num = models.CharField(max_length=12)
    coupon = models.ManyToManyField(Coupon, null=True, blank=True)
    class Meta:  
        db_table = "indi_cust"  

class Corp_cust(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    employee_id = models.DecimalField(max_digits=32,decimal_places=0)
    corp = models.ForeignKey(Corporation, on_delete=models.CASCADE)
    class Meta:  
        db_table = "corp_cust" 

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    idate = models.DateField()
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    record = models.OneToOneField(Rental_Record, on_delete=models.CASCADE)
    class Meta:  
        db_table = "invoice"

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pdate = models.DateField()
    method = models.CharField(max_length=10)
    card_num = models.DecimalField(max_digits=32,decimal_places=0)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=4,decimal_places=2,default=0.00)
    class Meta:  
        db_table = "payment"