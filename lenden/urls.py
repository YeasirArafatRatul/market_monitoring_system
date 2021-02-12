from django.urls import path, include
from django.conf import settings


from .views import *
from django.conf.urls.static import static

app_name = "lenden"


urlpatterns = [
    path('add-chalan/', AddChalanView.as_view(), name='add-chalan'),
    path('add-sales/', AddSalesView.as_view(), name='add-sales'),
    path('import-record/<int:pro_id>/<str:time>', ImportRecordView.as_view(),
         name='import-records'),
    path('sales-record/<int:pro_id>/<str:time>', SalesRecordView.as_view(),
         name='sales-record'),
         
    path('confirm/<int:id>', confirm,
         name='confirm'),
    path('details-of-product/<int:pro_id>',

    DifferenceBetweenWholeSaleRetailerMarketView.as_view(), name="details-of-two-market"),
    path('pending-records', PendingBuyingRecodrs.as_view(), name='pending-records'),

    path('mark-as-read',mark_as_read,name='mark_as_read'),
]
