from django.urls import path, include
from django.conf import settings


from .views import *
from django.conf.urls.static import static

app_name = "lenden"


urlpatterns = [
    path('add-product/', AddProductView.as_view(), name='add-product'),
    path('my-products/', ProductListView.as_view(), name='my-products'),

]