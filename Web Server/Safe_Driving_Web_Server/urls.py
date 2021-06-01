"""Safe_Driving_Web_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from main import views


urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    path('admin/signup/',views.signupuser,name="signupuser"),

    #general
    path('',views.home,name="home"),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    #Auth
    path('logout/',views.logoutuser,name="logoutuser"),
    path('logout/auto',views.autologout,name="autologout"),

    #car
    path('car/search',views.searchCar,name="searchCar"),
    path('car/searchCarXss',views.searchCarXss,name="searchCarXss"),


    #Customer --> CustomerAdd CustomerView CustomerEdit CustomerSearch
    path('customer/add',views.CustomerAdd,name="CustomerAdd"),
    path('customer/search',views.CustomerSearch,name="CustomerSearch"),
    path('customer/Edit/<int:customer_pk>',views.customerEdit,name="customerEdit"),
    path('customer/View/<int:customer_pk>',views.customerView,name="customerView"),
    
    #Customer --> customerSearchCar customerAddCar
    path('customer/View/<int:customer_pk>/SearchCar',views.customerSearchCar,name="customerSearchCar"),
    path('customer/View/<int:customer_pk>/AddCar',views.customerAddCar,name="customerAddCar"),
        #error
    path('customer/View/<int:customer_pk>/<str:number_car>/<int:error_code>',views.customerSearchCar_error,name="customerSearchCar_error"),

    #car customerRemoveCar
    path('customer/OwnershipChange/<int:car_pk>/<str:new_id>',views.OwnershipChangeCar,name="OwnershipChangeCar"),

    #ServiceCenters
    path('ServiceCenters/',views.ServiceCenters,name="ServiceCenters"),

    #update data from device

    path('updatedata/',views.updateData,name="updateData"),

    #change Password
    path('cpwd/<int:dev_id>',views.cpwd,name="cpwd"),

]
