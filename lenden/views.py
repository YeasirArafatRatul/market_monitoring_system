from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .forms import *
from django.core.exceptions import ValidationError
from lenden.models import Chalan
from django.db.models import Avg, Sum
from django.http import HttpResponse
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

        # print(type(user_total_sell_product_quantity))
        # print(user_total_sell_product_quantity + form.cleaned_data['quantity'])
        # print(user_product_total_quantity)

        if user_total_sell_product_quantity == None:
            user_total_sell_product_quantity = 0

        buyer = User.objects.filter(
            trade_license_no=form.instance.buyer).first()
        print(buyer)
        if user_product_total_quantity >= (user_total_sell_product_quantity + form.cleaned_data['quantity']):
            form.save()
            notify.send(user, recipient=buyer,
                        verb="has issued a selling record on your name")
        else:
            raise forms.ValidationError(
                "You don't have enough product to sell")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ImportRecordView(ListView):
    model = Chalan
    # USE THE TEMPLATE You want to render
    template_name = 'lenden/import_product_details.html'
    context_object_name = 'chalans'

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['pro_id'])
        return Product.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_chalan_for_individual_product = Chalan.objects.filter(
            owner=self.request.user, product=self.id)

        average_price = SellProduct.objects.filter(
            seller=self.request.user, product=self.id).aggregate(Avg('price'))['price__avg']

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


class SalesRecordView(ListView):
    model = SellProduct
    # USE THE TEMPLATE You want to render
    template_name = 'lenden/sale_product_details.html'
    context_object_name = 'chalans'
    paginate_by = 3

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['pro_id'])
        return Product.objects.filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_sales_for_individual_product = SellProduct.objects.filter(
            seller=self.request.user, product=self.id)

        average_price = SellProduct.objects.filter(
            seller=self.request.user, product=self.id).aggregate(Avg('price'))['price__avg']

        user_product_total_quantity = Chalan.objects.filter(
            owner=self.request.user, product=self.id).aggregate(Sum('quantity'))['quantity__sum']

        user_total_sell_product_quantity = SellProduct.objects.filter(
            seller=self.request.user, product=self.id).aggregate(Sum('quantity'))['quantity__sum']

        if user_total_sell_product_quantity == None:
            user_total_sell_product_quantity = 0

        if SellProduct.objects.filter(seller=self.request.user, product=self.id).exists():
            unit_for_chalan = SellProduct.objects.filter(
                seller=self.request.user, product=self.id).values('unit').first()['unit']
            context['unit'] = unit_for_chalan
        else:
            context['message'] = "NO SELL IS RECORDED FOR THIS PRODUCT"

        context['total'] = user_product_total_quantity

        context['sold'] = user_total_sell_product_quantity
        context['available'] = (user_product_total_quantity -
                                user_total_sell_product_quantity)
        context['average'] = average_price
        context['sales'] = my_sales_for_individual_product

        return context

# TO SAVE a CHALAN object from SELLPRODUCT object:


class AutomatedChalanProductAddView(LoginRequiredMixin, CreateView):
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


def confirm(request, id):
    obj = SellProduct.objects.get(id=id)
    print("HELLLLLLLLLLLLLLLLO")
    print(obj.pending)
    obj.pending = False
    obj.save(update_fields=["pending"])

    @receiver(post_save, sender=SellProduct)
    def create_object(sender, instance, created, **kwargs):
        user = User.objects.get(trade_license_no=instance.buyer)
        print(user)
        if created and instance.pending == False:
            Chalan.objects.create(owner=user, product=instance.product, quantity=instance.quantity,
                                  unit=instance.unit, price=instance.price, import_date=instance.sell_date, imported_from=instance.seller.username)
            post_save.connect(create_object, sender=SellProduct)

    create_object(sender=SellProduct, instance=obj, created=True)
    return HttpResponse("Done")
