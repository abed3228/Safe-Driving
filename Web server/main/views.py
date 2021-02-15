from django.contrib.auth import forms
from django.db.utils import InternalError
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash

from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm,DetailsForm,CarForm
from .models import Customer, Store

import urllib.request 
import ssl
import json

#from .forms import TodoForm,DeviceForm,TapForm
#from .models import Todo,Blog,Devices,Status,Tap

# Create your views here.

def home(request):
	if request.method == 'POST':
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		if user is None:
			return render(request,'main/home.html',{'form':AuthenticationForm(),'error':'Username and password did not match'})
		else:
			login(request,user)
			return redirect('home')
    
	return render(request,'main/home.html')

def contact(request):
	return render(request,'main/contact.html')

def about(request):
	return render(request,'main/about.html')

@login_required
def signupuser(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		form_1 = DetailsForm(request.POST)
		user_object=0
		if form.is_valid() and form_1.is_valid:
			try:
				form.save()
				username = form.cleaned_data['username']
				password = form.cleaned_data['password1']
				user = authenticate(username=username, password=password)
				user_object=user
				store = form_1.save(commit=False)
				store.user = request.user
				store.save()
				messages.success(request, ('You Have Registered...'))
				return redirect('home')
			except:
				user_object.delete()
				print("error IN")
				context = {'form': form, 'form_1':form_1,'error':'Data error'}
				return render(request , 'main/authentication/signupuser.html' ,context )
		else:
			user_object.delete()
			print("error")
			context = {'form': form, 'form_1':form_1,'error':'Data error'}
			return render(request , 'main/authentication/signupuser.html' ,context )
	else:
		form = SignUpForm()
		form_1=DetailsForm()
		context = {'form': form, 'form_1':form_1}
		return render(request, 'main/authentication/signupuser.html', context)
    
@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def search(request):
	if request.method == 'GET' and request.GET.get('query'):
		number_car = request.GET.get('query')
		print(number_car)
		api_start =  'https://data.gov.il/api/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3&filters={"mispar_rechev":"'
		api_end = '"}'
		api= api_start+number_car+api_end
		ssl._create_default_https_context = ssl._create_unverified_context
		x =  urllib.request.urlopen(api) 
		raw_data = x.read()
		encoding = x.info().get_content_charset('utf8')
		data = json.loads(raw_data.decode(encoding))
		dic = data.get("result").get("records")
		form = CarForm()

		if dic:
#			print(dic[0]["mispar_rechev"])
#			print(dic[0]["tozeret_nm"])
#			print(dic[0]["kinuy_mishari"])
#			print(dic[0]["ramat_gimur"])
#			print(dic[0]["tzeva_rechev"])
#			print(dic[0]["sug_delek_nm"])
#			print(dic[0]["baalut"])
#			print(dic[0]["tokef_dt"])

			context = {
			'form':form,
			'car_number':dic[0]["mispar_rechev"],
			'car_manufacturer':dic[0]["tozeret_nm"],
			'car_model':dic[0]["kinuy_mishari"],
			'car_finishing':dic[0]["tzeva_rechev"],
			'car_color':dic[0]["sug_delek_nm"],
			'car_fuel_type':dic[0]["baalut"],
			'car_test':dic[0]["tokef_dt"]
			}
			return render(request, 'main/search.html',context)
		else:
			print("car not exsit")
			context = {'error': "car not exsit"}
			return render(request, 'main/search.html',context)
	
	elif request.method == 'POST':
		print("POST")
		form = CarForm(request.POST)
		print(form)
		if form.is_valid():
			try:
				customer = form.cleaned_data['customer']
				print(customer)
				context = {'success': "The car was successfully maintained"}
				return render(request, 'main/search.html',context)
			except:
				context = {'error': "Problem saving data"}
				return render(request, 'main/search.html',context)
		else:
			context = {'error': "Problem data"}
			return render(request, 'main/search.html',context)

	else:	
		return render(request, 'main/search.html')


@login_required
def addcar(request):
    if request.method == 'POST':
	    print("POST addcar")
	    form = CarForm(request.POST)
	    print(form)
	    return render(request,'main/search.html')
    return render(request,'main/search.html')