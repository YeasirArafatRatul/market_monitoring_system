from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from .forms import *
# Create your views here.



class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'products'
    paginate_by = 10

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        products = Product.objects.filter(owner_id=self.request.user.id)
        for pro in products:
            print(pro.name)

        return self.model.objects.filter(owner_id=self.request.user.id)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class AddProductView(LoginRequiredMixin, CreateView):
    form_class = AddProductForm
    template_name = 'lenden/addproduct.html'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        request = self.request
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

