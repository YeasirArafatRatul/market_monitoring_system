from django.contrib import admin
from .models import *
# Register your models here.


class SellProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'buyer',
                    'product', 'unit', 'price', 'pending']


admin.site.register(Product)
admin.site.register(Chalan)
admin.site.register(SellProduct, SellProductAdmin)
