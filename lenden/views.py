from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import *
from django.core.exceptions import ValidationError
# Create your views here.


class AddChalanView(LoginRequiredMixin, CreateView):
    form_class = AddChalanForm
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


class AddSalesView(LoginRequiredMixin, CreateView):
    form_class = AddSalesForm
    template_name = 'lenden/demo-form.html'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        request = self.request
        form.instance.seller = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context
