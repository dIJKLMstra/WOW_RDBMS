from django import forms
from .models import Customer, Indi_cust, Corp_cust, Payment,Vehicle
from .models import Rental_Record
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['fname', 'lname', 'country', 'state', 'city',
             'street', 'zipcode', 'email', 'phone', 'cust_type']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'make','model','year','vin','class_id',
                  'location','lp_num']

    def clean(self):
        # add constraint
        if len(self.cleaned_data["vin"]) != 17:
            raise forms.ValidationError("VIN needs exact 17 numbers")
        return self.cleaned_data


class Indi_CustForm(forms.ModelForm):
    class Meta:
        model = Indi_cust
        fields = ['dl_num', 'insur_com_name', 'insur_polic_num']

class Corp_custForm(forms.ModelForm):
    class Meta:
        model = Corp_cust
        fields = ['employee_id', 'corp']

class RecordForm(forms.ModelForm):
    class Meta:
        model = Rental_Record
        fields = ['customer', 'pickup_date', 'dropoff_date', 'start_odo',
            'end_odo', 'odo_limit', 'vehicle', 'pu_location', 'do_location' ]
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'dropoff_date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def clean(self):
        # add constraint
        if(self.cleaned_data['dropoff_date'] < self.cleaned_data['pickup_date']):
            self.add_error("dropoff_date", "Dropoff date needs later than pickup date.")
        if(self.cleaned_data['end_odo'] < self.cleaned_data['start_odo']):
            self.add_error("end_odo", "End odometer needs larger than start odometer.")
        return self.cleaned_data
