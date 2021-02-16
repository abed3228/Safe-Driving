from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receive


# Create your models here.

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

#    print(dic[0]["mispar_rechev"]) - car number - מספר רכב 
#    print(dic[0]["tozeret_nm"]) - manufacturer - יצרן
#    print(dic[0]["kinuy_mishari"]) - model -דגם 
#    print(dic[0]["ramat_gimur"]) - Automotive Finishing - רמת גימור
#    print(dic[0]["tzeva_rechev"]) - color - צבע
#    print(dic[0]["sug_delek_nm"]) - fuel type - סוג דלק
#    print(dic[0]["baalut"]) - own  type - סוג בעלים
#    print(dic[0]["tokef_dt"]) - test - רישוי שנתי

class Customer(models.Model):
    customer_name = models.CharField(max_length=50, blank=True)
    customer_id = models.CharField(unique=True,max_length=30, blank=True)
    customer_phone = models.CharField(max_length=12, blank=True)
    customer_email = models.EmailField()
    customer_country = models.CharField(max_length=30, blank=True)
    customer_city = models.CharField(max_length=30, blank=True)
    customer_address = models.CharField(max_length=30, blank=True)
    customer_address_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
            return self.customer_id


class Car(models.Model):
    customer = models.ForeignKey(to=Customer,on_delete=models.CASCADE)
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
    def __str__(self):
            return self.car_number

