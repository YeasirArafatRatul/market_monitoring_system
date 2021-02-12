from django.contrib import admin
from .models import *
# Register your models here.

class ChalanAdmin(admin.ModelAdmin):
    list_display = ['owner','product','quantity']
class SellProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'buyer',
                    'product', 'quantity', 'unit', 'price', 'pending']


admin.site.register(Product)
admin.site.register(Chalan,ChalanAdmin)
admin.site.register(SellProduct, SellProductAdmin)
