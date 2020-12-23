from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['trade_license_no', 'username', ]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
