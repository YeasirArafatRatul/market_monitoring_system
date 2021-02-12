from time import strftime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from accounts.models import User
from lenden.models import *
from django.db.models import Avg, Sum

from rest_framework import generics
from admin_site.api.serializers import ChalanSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class ChalanListView(ListView):
    model = Chalan
    # USE THE TEMPLATE You want to render
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'chalans'

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['pro_id'])
        return Chalan.objects.filter(product=self.id)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['total'] = Chalan.objects.filter(product=self.id
                                                 ).aggregate(Sum('quantity'))['quantity__sum']
        context['average_price'] = Chalan.objects.filter(product=self.id
                                                         ).aggregate(Avg('price'))['price__avg']
        context['unit_of_total'] = Chalan.objects.filter(
            product=self.id).first()

        return context


class ProductSellsView(ListView):
    model = Chalan
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'chalans'
    paginate_by = 10

    def get_queryset(self):
        url = self.request.META.get("HTTP_REFERER")  # get last url
        # print(url)
        return self.model.objects.filter()


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


class ChartView(ListView):
    models = Chalan
    template_name = 'dashboard/chart.html'

    month = strftime('%m')
    year = strftime('%Y')

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['id'])
        data = {}
        i = 1
        for i in range(1, 13):
            avg_of_month = Chalan.objects.filter(product=self.id, import_date__month=str(i), import_date__year=self.year
                                                 ).aggregate(Avg('price'))['price__avg']
            new_data = {(months[i-1]): avg_of_month}
            data.update(new_data)
        print(data)
        return JsonResponse(data, safe=False)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context[""] = data
    #     return context


# API ENDPOINT : http://127.0.0.1:8000/api/chalan-chart/<product-id>

# Average Importing Price OF Importers
class ChalanChart(APIView):
    year = strftime('%Y')

    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, id, format=None):
        self.id = get_object_or_404(Product, id=self.kwargs['id'])
        print(self.id)
        serializer = {}
        i = 1
        for i in range(1, 13):
            avg_of_month = Chalan.objects.filter(product=self.id, import_date__month=str(i), import_date__year=self.year
                                                 , owner__role='importer').aggregate(Avg('price'))['price__avg']

            new_data = {(months[i-1]): avg_of_month}
            serializer.update(new_data)
        return Response(serializer)

#   Average selling price of importers
# API ENDPOINT : http://127.0.0.1:8000/api/importers-selling-chart/<product-id>
class ImportersSellingChart(APIView):
    year = strftime('%Y')

    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, id, format=None):
        self.id = get_object_or_404(Product, id=self.kwargs['id'])
        print(self.id)
        serializer = {}
        i = 1
        for i in range(1, 13):
            avg_of_month = SellProduct.objects.filter(product=self.id, sell_date__month=str(i), sell_date__year=self.year
                                                 , seller__role='importer').aggregate(Avg('price'))['price__avg']

            new_data = {(months[i-1]): avg_of_month}
            serializer.update(new_data)
        return Response(serializer)


#   Average selling price of wholesellers
# API ENDPOINT : http://127.0.0.1:8000/api/wholesellers-selling-chart/<int:id>
class WholesellersSellingChart(APIView):
    year = strftime('%Y')

    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, id, format=None):
        self.id = get_object_or_404(Product, id=self.kwargs['id'])
        print(self.id)
        serializer = {}
        i = 1
        for i in range(1, 13):
            avg_of_month = SellProduct.objects.filter(product=self.id, sell_date__month=str(i), sell_date__year=self.year,
                                                 seller__role='wholeseller').aggregate(Avg('price'))['price__avg']

            new_data = {(months[i-1]): avg_of_month}
            serializer.update(new_data)
        return Response(serializer)
