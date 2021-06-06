from django.contrib.auth import forms
from django.db.utils import InternalError
from django.forms.widgets import EmailInput
from django.shortcuts import get_list_or_404, render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash

from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm,DetailsForm,ContactForm,CustomerForm,CarForm,DeviceForm,DataForm,PwdForm
from .models import Customer, Store,Car,Device,Data

from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta

from django.db.models import Q

import urllib.request 
import ssl
import json
import os
from twilio.rest import Client
#view safe
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

#from .forms import TodoForm,DeviceForm,TapForm
#from .models import Todo,Blog,Devices,Status,Tap.

#api
account_sid = ''
auth_token =  ''
client = Client(account_sid, auth_token)

def car_api(number_car):
	api_start =  'https://data.gov.il/api/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3&filters={"mispar_rechev":"'
	api_end = '"}'
	api= api_start+number_car+api_end
	ssl._create_default_https_context = ssl._create_unverified_context
	x =  urllib.request.urlopen(api) 
	raw_data = x.read()
	encoding = x.info().get_content_charset('utf8')
	data = json.loads(raw_data.decode(encoding))
	dic = data.get("result").get("records")
	return dic

def sms(name,phone,old_phone,car,code_sms):
	print(name)
	print(phone)
	print(old_phone)
	print(car)
	print(code_sms)
	#add car
	if code_sms == 1:
		text = "Hello "+name+ "\ncar number: " + car + "\nsuccessfully add to system \nyou can now use our system \nThank you safdrive."
	#add customer
	elif code_sms == 2:
		text ="Dear " + name +" \nwelcome to safdrive \nThank you for joining us \n Always at your service \nsafdrive." 
	elif code_sms == 3:
		text = "Hello "+name+ "\ncar number: " + car + "\nsuccessfully remove from your id \nThank you safdrive."
	message = client.messages.create(
    body=text,
    from_='SafeDriving',
    to="+"+phone
	)
	print(message.sid)
#125 +972 525598699 1234 12345678
def update_dev(dev_contry,dev_phone,id,contry,phone,pwd,car):
	text=""
	phone_send=""
	if contry[0] != "+":
		text=str(id)+"+"+str(contry)+str(phone)+str(pwd)+str(car)	
	else:
		text=str(id)+str(contry)+str(phone)+str(pwd)+str(car)
	
	if dev_contry[0] != "+":
		phone_send="+"+str(dev_contry)+str(dev_phone)
	else:
		phone_send=str(dev_contry)+str(dev_phone)
		
	print(text)
	message = client.messages.create(
    body=text,
    from_='SafeDriving',
    #to=phone_send
	to="+972525598699"
	)
	print(message.sid)



#api-end
# Create your views here.

def home(request):
	if request.method == 'POST':
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		if user is None:
			return render(request,'main/home.html',{'form':AuthenticationForm(),'message':'Username and password','message_1': 'did not match'})
		else:
			login(request,user)
			return redirect('home')
    
	return render(request,'main/home.html')

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		try:
			form.save()
			context = {'message':'Thank you!','message_1':'We will contact you soon','message_2':'Estimated duration: up to 5 business days'}
			return render(request,'main/home.html', context )
		except ValueError:
			return render(request,'main/contact.html', {'form':ContactForm(),'message':'Error!!','message_1':'Data error'} )
	return render(request,'main/contact.html', {'form':ContactForm()})

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
        return render(request,'main/home.html',{'message':'Thank you!','message_1': 'Goodbye!'})


@login_required
def searchCar(request):
	try:
		if request.method == 'GET' and request.GET.get('query'):
			number_car = request.GET.get('query')
			if Car.objects.filter(car_number = number_car).exists():
					car_pk = Car.objects.filter(car_number = number_car)[0].id
					car = get_object_or_404(Car,pk=car_pk)
					customer_pk = Customer.objects.filter(customer_identification=car.customer_identification)[0].id
					customer = get_object_or_404(Customer,pk=customer_pk)
					context = {
						'car_number':car.car_number,
						'car_manufacturer':car.car_manufacturer,
						'car_model':car.car_model,
						'car_finishing':car.car_finishing,
						'car_color':car.car_color,
						'car_fuel_type':car.car_fuel_type,
						'car_test':car.car_test,
						'car_year':car.car_year,
						'car_owner':car.car_owner,
						'car_type':car.car_type,
						'id':car.customer_identification,
						'customer':customer,
						'car_pk':car_pk,
					}
					return render(request, 'main/searchCar.html',context)
			else:
				dic = car_api(number_car)
				if dic:
					context = {
					'car_number':dic[0]["mispar_rechev"],
					'car_manufacturer':dic[0]["tozeret_nm"],
					'car_model':dic[0]["kinuy_mishari"],
					'car_finishing':dic[0]["ramat_gimur"],
					'car_color':dic[0]["tzeva_rechev"],
					'car_fuel_type':dic[0]["sug_delek_nm"],
					'car_test':dic[0]["tokef_dt"],
					'car_year':dic[0]["shnat_yitzur"],
					'car_owner':dic[0]["baalut"],
					'car_type':dic[0]["sug_degem"]
					}
					return render(request, 'main/searchCar.html',context)
				else:
					print("car not exsit")
					context = {'message': 'Sorry!','message_1': 'car not exsit'}
					return render(request, 'main/searchCar.html',context)
		elif request.method == 'GET' and request.GET.get('query_id'):
			new_id = request.GET.get('query_id')
			if Customer.objects.filter(customer_identification=new_id).exists():
				query_id_car = request.GET.get('query_id_car')
				car_pk = Car.objects.filter(car_number = query_id_car)[0].id
				car_id = get_object_or_404(Car,pk=car_pk)
				car_id=car_id.customer_identification
				if car_id != new_id:
					return redirect('OwnershipChangeCar',car_pk,new_id )
				else:
					context = {'message': 'Error - The same ID!','message_1': '',}
					return render(request, 'main/searchCar.html',context)
			else:
				context = {'message': 'Error - Ownership Change Car!','message_1': 'customer id not exsit' , 'message_2':'move to customer add '}
				return render(request, 'main/searchCar.html',context)
		else:
			return render(request, 'main/searchCar.html')
	except:
		context = {'message': 'Data Error','message_1': 'searchCar'}
		
		return render(request, 'main/searchCar.html',context)


@login_required
def searchCarXss(request):
	return render(request, 'main/home.html')

@login_required
def autologout(request):
	logout(request)
	context = {'message': 'Where are you?','message_1': '','message_2': 'Automatic Logout after 10 minutes'}
	return render(request, 'main/home.html',context)

@login_required
def CustomerAdd(request):
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		error_exists="exists: "
		id_ex =  request.POST.get('customer_identification')
		con = {
				'customer_name':request.POST.get('customer_name'),
				'customer_last_name':request.POST.get('customer_last_name'),
				'customer_date':request.POST.get('customer_date'),
				'customer_address':request.POST.get('customer_address'),
				'customer_address_number':request.POST.get('customer_address_number'),
				'customer_city':request.POST.get('customer_city'),
				'customer_post_code':request.POST.get('customer_post_code'),
				'customer_state':request.POST.get('customcustomer_stateer_name'),
				'customer_country':request.POST.get('customer_country'),
				'customer_fist_name_contact_details':request.POST.get('customer_fist_name_contact_details'),
				'customer_last_name_contact_details':request.POST.get('customer_last_name_contact_details'),
				'customer_code_phone':request.POST.get('customer_code_phone'),
				'customer_phone':request.POST.get('customer_phone'),
				'customer_email':request.POST.get('customer_email'),
				'customer_identification':request.POST.get('customer_identification'),
		}
		try:
			if Customer.objects.filter(customer_identification=id_ex).exists():
				error_exists=error_exists + " ID ,"
				con["customer_id"]=""
				context = {'message': 'ERROR!','message_1': error_exists,'con':con}
				return render(request, 'main/CustomerAdd.html',context)
			else:
				form.save()
				#sms_car(name,phone,old_phone,car,code_sms)
				try:
					print("try sms cus")
					cus_pk = Customer.objects.filter(customer_identification=id_ex)[0].pk
					cus = get_object_or_404(Customer,pk=cus_pk)
					name = cus.customer_last_name_contact_details + " " + cus.customer_fist_name_contact_details
					phone = cus.customer_code_phone+cus.customer_phone
					sms(name,phone,0,0,2)
				except:
					None
				context = {'message': 'Saved successfully','message_1': ''}
				return render(request, 'main/home.html',context)
		except:
			error_exists="ERROR in SAVE DATA "
			id_ex =  request.POST.get('customer_identification')
			con = {
				  'customer_name':request.POST.get('customer_name'),
				  'customer_last_name':request.POST.get('customer_last_name'),
				  'customer_date':request.POST.get('customer_date'),
				  'customer_address':request.POST.get('customer_address'),
    			  'customer_address_number':request.POST.get('customer_address_number'),
				  'customer_city':request.POST.get('customer_city'),
				  'customer_post_code':request.POST.get('customer_post_code'),
				  'customer_state':request.POST.get('customcustomer_stateer_name'),
				  'customer_country':request.POST.get('customer_country'),
				  'customer_fist_name_contact_details':request.POST.get('customer_fist_name_contact_details'),
				  'customer_last_name_contact_details':request.POST.get('customer_last_name_contact_details'),
				  'customer_code_phone':request.POST.get('customer_code_phone'),
				  'customer_phone':request.POST.get('customer_phone'),
				  'customer_email':request.POST.get('customer_email'),
				  'customer_identification':request.POST.get('customer_identification'),

			}
			context = {'message': 'ERROR!','message_1': error_exists,'con':con}
			return render(request, 'main/CustomerAdd.html',context)
	else:
		form = CustomerForm()
		return render(request, 'main/CustomerAdd.html',{'form':form})

@login_required
def CustomerSearch(request):
	if request.method == 'GET' and request.GET.get('query'):
		id_q=request.GET.get('query')
		if not Customer.objects.filter(customer_identification=id_q).exists():
			return render(request, 'main/CustomerSearch.html',{'con':id_q})
		else:
			customer = Customer.objects.filter(customer_identification=id_q)
			customer = customer[0].pk
			return redirect('customerView',customer)
	else:
		return render(request, 'main/CustomerSearch.html')


@login_required
def customerView(request,customer_pk):
	customer = get_object_or_404(Customer,pk=customer_pk)
	id=customer.customer_identification
	cars = Car.objects.filter(customer_identification=id)
	#cars.union(Device.objects.all())
	#print(cars.query)
	#dev = Device.objects.filter(course__course_name__exact="cars")
	#print(dev.query)
	return render(request, 'main/customerView.html',{'customer':customer,'cars':cars})

@login_required
def customerEdit(request,customer_pk):
	if request.method == "GET":
		customer = get_object_or_404(Customer,pk=customer_pk)
		form = CustomerForm(instance=customer)
		return render(request, 'main/customerEdit.html',{'customer':customer, 'form':form})
	else:
		customer = Customer.objects.get(pk=customer_pk)
		
		form = CustomerForm(request.POST,instance=customer)
		customer.customer_name = request.POST.get('customer_name')
		customer.customer_last_name = request.POST.get('customer_last_name')
		customer.customer_identification = customer.customer_identification
		customer.customer_date = request.POST.get('customer_date')
		customer.customer_address = request.POST.get('customer_address')
		customer.customer_address_number = request.POST.get('customer_address_number')
		
		customer.customer_city = request.POST.get('customer_city')
		customer.customer_post_code = request.POST.get('customer_post_code')
		customer.customer_state = request.POST.get('customer_state')
		customer.customer_country = request.POST.get('customer_country')
		customer.customer_fist_name_contact_details = request.POST.get('customer_fist_name_contact_details')
		customer.customer_last_name_contact_details = request.POST.get('customer_last_name_contact_details')
		
		customer.customer_code_phone = request.POST.get('customer_code_phone')
		customer.customer_phone = request.POST.get('customer_phone')
		customer.customer_email = request.POST.get('customer_email')

		customer.save()
		
		return redirect('customerView',customer_pk)
		

@login_required
def customerSearchCar(request,customer_pk):
	customer = get_object_or_404(Customer,pk=customer_pk)
	if request.method == 'GET' and request.GET.get('query'):
		number_car = request.GET.get('query')
		dic = car_api(number_car)
		if dic:
			if Car.objects.filter(car_number = dic[0]["mispar_rechev"]).exists():
				print("car  exsit")
				context = {'message': 'Sorry!','message_1': 'car exsit','customer':customer}
				return render(request, 'main/customerSearchCar.html',context)
			else:
				form = CarForm()
				id=customer.customer_identification
				context = {
				'car_year':dic[0]["shnat_yitzur"],
				'car_owner':dic[0]["baalut"],
				'car_type':dic[0]["sug_degem"],
				'car_number':dic[0]["mispar_rechev"],
				'car_manufacturer':dic[0]["tozeret_nm"],
				'car_model':dic[0]["kinuy_mishari"],
				'car_finishing':dic[0]["ramat_gimur"],
				'car_color':dic[0]["tzeva_rechev"],
				'car_fuel_type':dic[0]["sug_delek_nm"],
				'car_test':dic[0]["tokef_dt"],
				'customer_identification':id,
				'customer':customer,
				'form':form,
				}
				
				return render(request, 'main/customerSearchCar.html',context)
		else:
			print("car not exsit")
			context = {'message': 'Sorry!','message_1': 'car not exsit','customer':customer}
			return render(request, 'main/customerSearchCar.html',context)	
	else:
		return render(request, 'main/customerSearchCar.html',{'customer':customer})

@login_required
def customerSearchCar_error(request,customer_pk,number_car,error_code):
	customer = get_object_or_404(Customer,pk=customer_pk)
	dic = car_api(number_car)
	if dic:
			form = CarForm()
			id=customer.customer_identification
			if error_code == 1:
				context = {
					'message': 'Error!',
					'message_1': 'serial number device not exists',
					
				}
			elif error_code == 2:
				context = {
					'message': 'Error!',
					'message_1': 'Data Error',
				}
			elif error_code == 3:
				context = {
				'message': 'Error!',
				'message_1': 'serial number device is taken',
				'message_2':'Please check the number again',
				}
			else:
				context = {'its':'dic'}
			context.update({
				'car_year':dic[0]["shnat_yitzur"],
				'car_owner':dic[0]["baalut"],
				'car_type':dic[0]["sug_degem"],
				'car_number':dic[0]["mispar_rechev"],
				'car_manufacturer':dic[0]["tozeret_nm"],
				'car_model':dic[0]["kinuy_mishari"],
				'car_finishing':dic[0]["ramat_gimur"],
				'car_color':dic[0]["tzeva_rechev"],
				'car_fuel_type':dic[0]["sug_delek_nm"],
				'car_test':dic[0]["tokef_dt"],
				'customer_identification':id,
				'customer':customer,
				'form':form,
			})
			return render(request, 'main/customerSearchCar.html',context)
	else:
		print("Error api")
		context = {'message': 'Sorry!','message_1': 'Error api','customer':customer}
		return render(request, 'main/customerSearchCar.html',context)	


@login_required
def customerAddCar(request,customer_pk):
	if request.method == 'POST':
		try:
			form = CarForm(request.POST)
			serial = request.POST.get('serial_number_car')
			dev_id = Device.objects.filter(serial_number_Device=serial)
			dev_id = dev_id[0].pk
			dev = get_object_or_404(Device,pk=dev_id)

			if dev.its_taken == False:
				try:
					dev.car_number_Device = request.POST.get('car_number')
					dev.its_taken=True
					dev.car_code_Device = request.POST.get('code_car')
					dev.save()
					form.save()
					#sms(name,phone,old_phone,car,code_sms)
					#update_dev(dev_contry,dev_phone,id,contry,phone,pwd,car)
					try:
						print("try sms")
						cus = get_object_or_404(Customer,pk=customer_pk)
						name = cus.customer_last_name_contact_details + " " + cus.customer_fist_name_contact_details
						phone = cus.customer_code_phone+cus.customer_phone
						update_dev(cus.customer_code_phone,cus.customer_phone,dev.serial_number_Device,dev.contact_country_Device,dev.contact_phone_Device,dev.car_code_Device,dev.car_number_Device)
						sms(name,phone,0,dev.car_number_Device,1)
						return redirect('customerView',customer_pk)
					except:
						None
				except:
					car = request.POST.get('car_number')
					return redirect('customerSearchCar_error',customer_pk,car,2)
			else:
				car = request.POST.get('car_number')
				return redirect('customerSearchCar_error',customer_pk,car,3)
		except:
			car = request.POST.get('car_number')
			return redirect('customerSearchCar_error',customer_pk,car,1)
	else:
		return redirect('home')



@login_required
def OwnershipChangeCar(request,car_pk,new_id):
	if request.method == 'POST':
		car = get_object_or_404(Car,pk=car_pk)
		customer_pk = Customer.objects.filter(customer_identification=new_id)[0].id
		new_cus=get_object_or_404(Customer,pk=customer_pk)
		try:
			car.customer_identification=new_id
			#new
			name_new = new_cus.customer_last_name_contact_details + " " + new_cus.customer_fist_name_contact_details
			phone_new=str(new_cus.customer_code_phone) + str(new_cus.customer_phone)
			sms(name_new,phone_new,0,car.car_number,1)
			#old
			customer_pk_old = Customer.objects.filter(customer_identification=car.customer_identification)[0].id
			cus_old = get_object_or_404(Customer,pk=customer_pk_old)
			name_old = cus_old.customer_last_name_contact_details + " " + cus_old.customer_fist_name_contact_details
			phone_old = str(cus_old.customer_code_phone) + str(cus_old.customer_phone)
			sms(name_old,phone_old,0,car.car_number,3)
			car.save()
			return redirect('customerView',customer_pk)
		except:
			context = {'message': 'ERROR!','message_1':'Error in ownership change car!'}
			return render(request, 'main/home.html',context)
	else:
		car = get_object_or_404(Car,pk=car_pk)
		customer_pk_old = Customer.objects.filter(customer_identification=car.customer_identification)[0].id
		customer_old = get_object_or_404(Customer,pk=customer_pk_old)
		
		customer_pk_new = Customer.objects.filter(customer_identification=new_id)[0].id
		customer_new = get_object_or_404(Customer,pk=customer_pk_new)
		context = {
			'car_year': car.car_year,
			'car_number':car.car_number,
			'car_manufacturer':car.car_manufacturer,
			'car_model':car.car_model,

			'cus_id_old':customer_old.customer_identification,
			'cus_country_old':customer_old.customer_country,
			'cus_first_name_old':customer_old.customer_name,
			'cus_last_name_old':customer_old.customer_last_name,
			'cus_code_phone_old':customer_old.customer_code_phone,
			'cus_phone_old':customer_old.customer_phone,
			
			'cus_id_old':customer_old.customer_identification,
			'cus_country_old':customer_old.customer_country,
			'cus_first_name_old':customer_old.customer_name,
			'cus_last_name_old':customer_old.customer_last_name,
			'cus_code_phone_old':customer_old.customer_code_phone,
			'cus_phone_old':customer_old.customer_phone,

			'cus_id_new':customer_new.customer_identification,
			'cus_country_new':customer_new.customer_country,
			'cus_first_name_new':customer_new.customer_name,
			'cus_last_name_new':customer_new.customer_last_name,
			'cus_code_phone_new':customer_new.customer_code_phone,
			'cus_phone_new':customer_new.customer_phone,

			'car_pk':car_pk,
			'new_id':new_id
		}
		return render(request, 'main/OwnershipChange.html',context)

#view safe
@xframe_options_exempt
def ok_to_load_in_a_frame(request):
    return HttpResponse("This page is safe to load in a frame on any site.")

#ServiceCenters
def ServiceCenters(request):
	list_store = Store.objects.all()
	return render(request, 'main/ServiceCenters.html',{'store':list_store})


	#/updatedata/?data_id=XXX&he_is_drunk=XXX&location_long=XXX&location_lac=XXX&level_alcohol_gl=XXX&level_alcohol_bac=XXX
#127.0.0.1:8000/updatedata/?data_id=125&he_is_drunk=True&location_long=31.952201&location_lac=34.901827&level_alcohol_gl=2.5&level_alcohol_bac=15
#www.alnkib.com/updatedata/?data_id=125&he_is_drunk=True&location_long=31.952201&location_lac=34.901827&level_alcohol_gl=2.5&level_alcohol_bac=15
#להוסיף סיסמה לזיהוי המכשיר לאבטחת מידע ביסיסי
def updateData(request):
    
	data_id = int(request.GET.get('data_id'))
	he_is_drunk = bool(request.GET.get('he_is_drunk'))
	location_long = request.GET.get('location_long')
	location_lac = request.GET.get('location_lac')
	level_alcohol_gl = request.GET.get('level_alcohol_gl')
	level_alcohol_bac = request.GET.get('level_alcohol_bac')

	if Device.objects.filter(serial_number_Device = data_id).exists():
		try:
			form = Data(data_id = data_id , he_is_drunk = he_is_drunk , location_long=location_long,location_lac = location_lac , level_alcohol_gl = level_alcohol_gl , level_alcohol_bac=level_alcohol_bac)
			form.save() 
		except:#במיקרה של שיגאה שליחת הודעה לקבלת מידע שוב
			print("error")
			None
	return redirect('home')

@login_required
def cpwd(request,dev_id):
	device_pk = Device.objects.filter(serial_number_Device = dev_id)[0].id
	device = get_object_or_404(Device,pk=device_pk)
	car = Car.objects.filter(serial_number_car=device)[0].id
	car_pk = get_object_or_404(Car,pk=car)
	 
	if request.method == 'POST':
		old_pwd = request.POST.get('old_pwd')
		new_pwd = request.POST.get('new_pwd')
		new_pwd_again = request.POST.get('new_pwd_again')
		lenMax = 4
		if len(old_pwd) == lenMax and len(new_pwd) == lenMax and len(new_pwd_again) == lenMax:
			if new_pwd_again != new_pwd and old_pwd != device.car_code_Device:
				context = {
				'dev':device,
				'car':car_pk,
				'message': 'Error!',
				'message_1': 'The new or old password',
				'message_2': 'does not match our database',
				}
				return render(request, 'main/cpwd.html',context)
			else:
				cus = Customer.objects.filter(customer_identification = car_pk.customer_identification)[0].id
				print(cus)
				cus_Details = get_object_or_404(Customer,pk=cus)
				try:
					device.car_code_Device=new_pwd
					update_dev(device.contact_country_Device,device.contact_phone_Device,device.serial_number_Device,cus_Details.customer_code_phone,cus_Details.customer_phone,device.car_code_Device,device.car_number_Device)
					device.save()
				except:
					return redirect('home')
				return redirect('customerView',cus)
		else:
			return redirect('home')
	else:
		context = {
			'dev':device,
			'car':car_pk,
		}
		return render(request, 'main/cpwd.html',context)
	return render(request, 'main/home.html')

