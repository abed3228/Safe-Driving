from django.contrib.auth import models
from django.forms import ModelForm
#from .models import Todo,Devices,Status,Tap
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Store,Customer,Contact,Car,Device,Data


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['contact_name','contact_email','contact_country','contact_phone','contact_message']

class DetailsForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name_store','email','phone_store','country_store','city_store',
				  'address_store','address_number_store','name_contact',
				  'phone_contact',]

class EditProfileForm(UserChangeForm):
	password = forms.CharField(label="",  widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = User
		fields = ('username', 'password',)


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2',)

	def __init__(self, *args, **kwargs):
	    super(SignUpForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['username'].widget.attrs['placeholder'] = 'User Name'
	    self.fields['username'].label = ''
	    self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

	    self.fields['password1'].widget.attrs['class'] = 'form-control'
	    self.fields['password1'].widget.attrs['placeholder'] = 'Password'
	    self.fields['password1'].label = ''
	    self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

	    self.fields['password2'].widget.attrs['class'] = 'form-control'
	    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
	    self.fields['password2'].label = ''
	    self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['customer_identification','car_number','car_manufacturer','car_model','car_finishing','car_color' 
    			  ,'car_fuel_type','car_test','car_year','car_owner','car_type','serial_number_car',
		]


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name','customer_last_name','customer_identification','customer_date','customer_address',
    			  'customer_address_number','customer_city','customer_post_code','customer_state',
				  'customer_country','customer_fist_name_contact_details',
				  'customer_last_name_contact_details','customer_code_phone','customer_phone','customer_email',
		]

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['car_number_Device','serial_number_Device',]

class DataForm(ModelForm):
    class Meta:
        model = Data
        fields = ['data_id','he_is_drunk','location_long','location_lac','level_alcohol_gl','level_alcohol_bac']

class PwdForm(ModelForm):
	model = Device
	fields = ['old_pwd','new_pwd','new_pwd_again'] 