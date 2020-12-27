from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .forms import *
from django.core.exceptions import ValidationError
from lenden.models import Chalan
from django.db.models import Avg, Sum
# Create your views here.


class AddChalanView(LoginRequiredMixin, CreateView):
    form_class = AddChalanForm
    template_name = 'lenden/add_chalan.html'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        request = self.request
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class AddSalesView(LoginRequiredMixin, CreateView):
    form_class = AddSalesForm
    template_name = 'lenden/add_sale.html'
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        user = self.request.user
        form.instance.seller = self.request.user
        product = form.cleaned_data['product']
        user_product_total_quantity = Chalan.objects.filter(
            owner=user, product_id=product).aggregate(Sum('quantity'))['quantity__sum']

        user_total_sell_product_quantity = SellProduct.objects.filter(
            seller=user, product_id=product).aggregate(Sum('quantity'))['quantity__sum']

        print(type(user_total_sell_product_quantity))
        print(user_total_sell_product_quantity + form.cleaned_data['quantity'])

        print(user_product_total_quantity)
        if user_product_total_quantity >= (user_total_sell_product_quantity + form.cleaned_data['quantity']):
            form.save()
        else:
            raise forms.ValidationError(
                "You don't have enough product to sell")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class MyProductListView(ListView):
    model = Chalan
    # USE THE TEMPLATE You want to render
    template_name = 'lenden/product_details.html'
    context_object_name = 'chalans'

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['pro_id'])
        return Product.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_chalan_for_individual_product = Chalan.objects.filter(
            owner=self.request.user, product=self.id)

        average_price = SellProduct.objects.filter(
            seller=self.request.user).aggregate(Avg('price'))['price__avg']

        user_product_total_quantity = Chalan.objects.filter(
            owner=self.request.user, product=self.id).aggregate(Sum('quantity'))['quantity__sum']

        user_total_sell_product_quantity = SellProduct.objects.filter(
            seller=self.request.user, product=self.id).aggregate(Sum('quantity'))['quantity__sum']

        if user_total_sell_product_quantity == None:
            user_total_sell_product_quantity = 0

        unit_for_chalan = Chalan.objects.filter(
            owner=self.request.user, product=self.id).values('unit').first()['unit']

        context['total'] = user_product_total_quantity
        context['unit'] = unit_for_chalan
        context['sold'] = user_total_sell_product_quantity
        context['available'] = (user_product_total_quantity -
                                user_total_sell_product_quantity)
        context['average'] = average_price
        context['chalans'] = my_chalan_for_individual_product
        print(context)
        return context
