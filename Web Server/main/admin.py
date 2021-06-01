from django.contrib import admin
from .models import Store,Customer,Contact,Car,Device,Data
# Register your models here.

class MainAdmin(admin.ModelAdmin):
    readonly_fields = ('created','date',)

admin.site.register(Store)

admin.site.register(Customer)

admin.site.register(Car)

admin.site.register(Contact)

admin.site.register(Device)

admin.site.register(Data)