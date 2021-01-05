from django.contrib import admin
from .models import Notice
# Register your models here.


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'notice_type']
    list_filter = ['notice_type', 'created_at']


admin.site.register(Notice, NoticeAdmin)
