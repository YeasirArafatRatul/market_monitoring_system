from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from accounts.models import User
from lenden.models import *
from django.db.models import Avg, Sum
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

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['id'])
        data = {}
        i = 1
        for i in range(1, 13):
            avg_of_month = Chalan.objects.filter(product=self.id, import_date__month=str(i)
                                                 ).aggregate(Avg('price'))['price__avg']
            new_data = {(months[i-1]): avg_of_month}
            data.update(new_data)
        print(data)
        return JsonResponse(data, safe=False)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context[""] = data
    #     return context
