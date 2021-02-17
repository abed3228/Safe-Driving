from django.contrib import admin
from .models import Store,Car,Customer
# Register your models here.

class MainAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Store)

admin.site.register(Customer)

admin.site.register(Car)

