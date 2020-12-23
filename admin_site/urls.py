from django.urls import path


from .views import *
from django.conf.urls.static import static

app_name = "admin_site"


urlpatterns = [
    path('filtered-chalan/<int:pro_id>',
         ChalanListView.as_view(), name='filtered-chalan'),
    path('all-chalans/',
         ProductSellsView.as_view(), name='all-chalans'),


]
