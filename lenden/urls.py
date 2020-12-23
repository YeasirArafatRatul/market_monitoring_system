from django.urls import path, include
from django.conf import settings


from .views import *
from django.conf.urls.static import static

app_name = "lenden"


urlpatterns = [
    path('add-chalan/', AddChalanView.as_view(), name='add-chalan'),


]
