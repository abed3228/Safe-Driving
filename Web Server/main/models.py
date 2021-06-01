from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

#from django.db.models.signals import post_save
#from django.dispatch import receive



class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    name_store = models.CharField(max_length=50, blank=True)
    phone_store = models.CharField(max_length=12, blank=True)
    country_store = models.CharField(max_length=30, blank=True)
    city_store = models.CharField(max_length=30, blank=True)
    address_store = models.CharField(max_length=30, blank=True)
    address_number_store = models.CharField(max_length=12, blank=True)
    name_contact = models.CharField(unique=True,max_length=30, blank=True)
    phone_contact = models.CharField(max_length=12, blank=True)
    note = models.CharField(max_length=30, blank=True)

    def __str__(self):
            return self.name_store


class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True)
    customer_last_name = models.CharField(max_length=50, blank=True)
    customer_identification = models.CharField(max_length=20)
    customer_date = models.DateField(blank=True)
    customer_address = models.CharField(max_length=30, blank=True)
    customer_address_number = models.CharField(max_length=30, blank=True)
    customer_city = models.CharField(max_length=30, blank=True)
    customer_post_code = models.CharField(max_length=30, blank=True)
    customer_state = models.CharField(max_length=30, blank=True)
    customer_country = models.CharField(max_length = 50, blank=True) 
    customer_fist_name_contact_details = models.CharField(max_length=50, blank=True)
    customer_last_name_contact_details = models.CharField(max_length=50, blank=True)
    customer_last_name_contact_details = models.CharField(max_length=50, blank=True)
    customer_code_phone = models.CharField(max_length=5, blank=True)
    customer_phone = models.CharField(max_length=15, blank=True)
    customer_email = models.EmailField()


    def __str__(self):
            return self.customer_identification + " | (" + str(self.pk) +")"

class Device(models.Model):
    car_number_Device = models.CharField(unique=True,max_length=12, blank=True) 
    serial_number_Device = models.IntegerField(unique=True,blank=True)
    contact_country_Device =  models.CharField(max_length=30, blank=True)
    contact_phone_Device =  models.CharField(max_length=30, blank=True)
    car_code_Device = models.CharField(max_length=4, blank=True)
    its_taken=models.BooleanField(default=False)
    def __str__(self):
            return str(self.serial_number_Device)

#    print(dic[0]["mispar_rechev"]) - car number - מספר רכב 
#    print(dic[0]["tozeret_nm"]) - manufacturer - יצרן
#    print(dic[0]["kinuy_mishari"]) - model -דגם 
#    print(dic[0]["ramat_gimur"]) - Automotive Finishing - רמת גימור
#    print(dic[0]["tzeva_rechev"]) - color - צבע
#    print(dic[0]["sug_delek_nm"]) - fuel type - סוג דלק
#    print(dic[0]["baalut"]) - own  type - סוג בעלים
#    print(dic[0]["tokef_dt"]) - test - רישוי שנתי
class Car(models.Model):
    customer_identification = models.CharField(max_length=20)
    car_number = models.CharField(unique=True,max_length=12, blank=True)
    car_manufacturer = models.CharField(max_length=30, blank=True)
    car_model =  models.CharField(max_length=30, blank=True)
    car_finishing =  models.CharField(max_length=30, blank=True)
    car_color =  models.CharField(max_length=30, blank=True)
    car_fuel_type =  models.CharField(max_length=30, blank=True)
    car_test =  models.CharField(max_length=30, blank=True)
    car_owner =  models.CharField(max_length=30, blank=True)
    car_type =  models.CharField(max_length=30, blank=True)
    car_year =  models.CharField(max_length=4, blank=True)
    serial_number_car  = models.CharField(max_length=10, blank=True)
    def __str__(self):
            return self.car_number

class Contact(models.Model):
    contact_name =  models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField()
    contact_country =  models.CharField(max_length=30, blank=True)
    contact_phone =  models.CharField(max_length=30, blank=True)
    contact_message =  models.TextField(blank=True)
    def __str__(self):
            return self.contact_email


class Data(models.Model):
    data_id = models.IntegerField(blank=True)
    he_is_drunk=models.BooleanField(blank=True)
    location_long =  models.CharField(max_length=30, blank=True)
    location_lac =  models.CharField(max_length=30, blank=True)
    level_alcohol_gl = models.CharField(max_length=30, blank=True)
    level_alcohol_bac = models.CharField(max_length=30, blank=True)
    date_update = models.DateTimeField(default=now, blank=True)
    def __str__(self):
            return str(self.date_update)