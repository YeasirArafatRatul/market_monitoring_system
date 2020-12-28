from django.urls import path, include
from django.conf import settings


from .views import *
from django.conf.urls.static import static

app_name = "lenden"


urlpatterns = [
    path('add-chalan/', AddChalanView.as_view(), name='add-chalan'),
    path('add-sales/', AddSalesView.as_view(), name='add-sales'),
    path('import-record/<int:pro_id>', ImportRecordView.as_view(),
         name='import-records'),
    path('sales-record/<int:pro_id>', SalesRecordView.as_view(),
         name='sales-records'),
    path('confirm/<int:id>', confirm,
         name='confirm'),
]
