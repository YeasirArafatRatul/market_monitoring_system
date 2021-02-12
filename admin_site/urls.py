from django.urls import path


from .views import *
from django.conf.urls.static import static
from .views import ChalanChart
app_name = "admin_site"


urlpatterns = [
    path('filtered-chalan/<int:pro_id>',
         ChalanListView.as_view(), name='filtered-chalan'),
    path('all-chalans/',
         ProductSellsView.as_view(), name='all-chalans'),
    path('chart/<int:id>',
         ChartView.as_view(), name='chart'),
    path('api/chalan-chart/<int:id>',
         ChalanChart.as_view(), name='chart'),

     path('api/wholesellers-selling-chart/<int:id>',
         WholesellersSellingChart.as_view(), name='chart'),

     path('api/importers-selling-chart/<int:id>',
         ImportersSellingChart.as_view(), name='chart'),


]
