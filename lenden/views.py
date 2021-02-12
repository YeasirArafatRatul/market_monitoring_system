from django.http import JsonResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from notifications.signals import notify
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .forms import *
from django.core.exceptions import ValidationError
from lenden.models import Chalan
from django.db.models import Avg, Sum
from django.http import HttpResponse
# Create your views here.
import datetime
from datetime import time
from time import strftime


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
        # print(buyer)
        if user_product_total_quantity != None:
            if user_product_total_quantity >= (user_total_sell_product_quantity + form.cleaned_data['quantity']):

                form.save()
                notify.send(user, recipient=buyer,
                            verb="has issued a buying record on your name")
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
        time = self.kwargs['time']
        print(time)
        today = strftime("%d")
        print(today)
        month = strftime('%m')
        year = strftime('%Y')
        if not self.request.user.role == '':
            print(self.request.user.role)
            if time == 'today':
                print("TODAYS DATA IS SHOWING")

                my_chalan_for_individual_product = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__day=today)

                average_price = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__day=today).aggregate(Avg('price'))['price__avg']
                print(average_price)
                print("This is type", type(average_price))

                user_product_total_quantity = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__day=today).aggregate(Sum('quantity'))['quantity__sum']

                user_total_sell_product_quantity = SellProduct.objects.filter(
                    seller=self.request.user, product=self.id, sell_date__day=today).aggregate(Sum('quantity'))['quantity__sum']

                unit_for_chalan = Chalan.objects.filter(
                    owner=self.request.user, product=self.id).values('unit').first()['unit']

            elif time == 'month':
                print("THIS MONTH DATA IS SHOWING")
                # print(type(month))

                my_chalan_for_individual_product = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__month=month)

                average_price = SellProduct.objects.filter(
                    seller=self.request.user, product=self.id, sell_date__month=month).aggregate(Avg('price'))['price__avg']
             

                user_product_total_quantity = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__month=month).aggregate(Sum('quantity'))['quantity__sum']

                user_total_sell_product_quantity = SellProduct.objects.filter(
                    seller=self.request.user, product=self.id, sell_date__month=month).aggregate(Sum('quantity'))['quantity__sum']

                unit_for_chalan = Chalan.objects.filter(
                    owner=self.request.user, product=self.id).values('unit').first()['unit']

            else:
                print("THIS YEARS DATA IS SHOWING")

                my_chalan_for_individual_product = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__year=year)

                average_price = SellProduct.objects.filter(
                    seller=self.request.user, product=self.id, sell_date__year=year).aggregate(Avg('price'))['price__avg']

                user_product_total_quantity = Chalan.objects.filter(
                    owner=self.request.user, product=self.id, import_date__year=year).aggregate(Sum('quantity'))['quantity__sum']

                user_total_sell_product_quantity = SellProduct.objects.filter(
                    seller=self.request.user, product=self.id, sell_date__year=year).aggregate(Sum('quantity'))['quantity__sum']

                unit_for_chalan = Chalan.objects.filter(
                    owner=self.request.user, product=self.id).values('unit').first()['unit']

            if user_product_total_quantity == None:
                user_product_total_quantity = 0
            if user_total_sell_product_quantity == None:
                user_total_sell_product_quantity = 0

            context['product'] = Product.objects.filter(
                id=self.kwargs['pro_id']).first()

            context['total'] = user_product_total_quantity
            context['unit'] = unit_for_chalan
            context['sold'] = user_total_sell_product_quantity
            context['available'] = (user_product_total_quantity -
                                    user_total_sell_product_quantity)
            if average_price != None:
                context['average'] = f"{average_price:.2f}"
            else:
                context['average'] = 0
            context['chalans'] = my_chalan_for_individual_product

# USER IS ADMIN
        else:
            if time == 'today':
                # print(today)
                print(" TODAY DATA IS SHOWING")
     
                my_chalan_for_individual_product = Chalan.objects.filter(
                    product=self.id, import_date__gte=datetime.date.today()).exclude(customs_clearance_no=None)

                average_price = Chalan.objects.filter(
                    product=self.id, import_date__gte=datetime.date.today()).exclude(customs_clearance_no=None).aggregate(Avg('price'))['price__avg']
          
                print(average_price)
                print("This is type",type(average_price))


                user_product_total_quantity = Chalan.objects.filter(
                    product=self.id, import_date__gte=datetime.date.today()).exclude(customs_clearance_no=None).aggregate(Sum('quantity'))['quantity__sum']

                user_total_sell_product_quantity = SellProduct.objects.filter(
                    product=self.id, sell_date__gte=datetime.date.today()).aggregate(Sum('quantity'))['quantity__sum']

            elif time == 'month':
                print("THIS MONTH DATA IS SHOWING")

                my_chalan_for_individual_product = Chalan.objects.filter(
                    product=self.id, import_date__month=month).exclude(customs_clearance_no=None)
                average_price = Chalan.objects.filter(
                    product=self.id, import_date__month=month).exclude(customs_clearance_no=None).aggregate(Avg('price'))['price__avg']
                print(average_price)

                user_product_total_quantity = Chalan.objects.filter(
                    product=self.id, import_date__month=month).exclude(customs_clearance_no=None).aggregate(Sum('quantity'))['quantity__sum']

                user_total_sell_product_quantity = SellProduct.objects.filter(
                    product=self.id, sell_date__month=month).aggregate(Sum('quantity'))['quantity__sum']

                if user_total_sell_product_quantity == None:
                    user_total_sell_product_quantity = 0

            else:
                my_chalan_for_individual_product = Chalan.objects.filter(
                    product=self.id, import_date__year=year).exclude(customs_clearance_no=None)
                average_price = Chalan.objects.filter(
                    product=self.id, import_date__year=year).exclude(customs_clearance_no=None).aggregate(Avg('price'))['price__avg']
                print(average_price)

                user_product_total_quantity = Chalan.objects.filter(
                    product=self.id, import_date__year=year).exclude(customs_clearance_no=None).aggregate(Sum('quantity'))['quantity__sum']

                user_total_sell_product_quantity = SellProduct.objects.filter(
                    product=self.id, sell_date__year=year,pending=False).aggregate(Sum('quantity'))['quantity__sum']

            unit_for_chalan = Chalan.objects.filter(
                product=self.id).values('unit').first()['unit']

            if user_product_total_quantity == None:
                user_product_total_quantity = 0
            if user_total_sell_product_quantity == None:
                user_total_sell_product_quantity = 0

            context['product_name'] = Product.objects.filter(
                id=self.kwargs['pro_id']).values('name').first()['name']

            context['product'] = Product.objects.filter(
                id=self.kwargs['pro_id']).first()

            context['total'] = user_product_total_quantity
            context['unit'] = unit_for_chalan
            context['sold'] = user_total_sell_product_quantity
            context['available'] = (user_product_total_quantity -
                                    user_total_sell_product_quantity)
            if average_price != None:
                context['average'] = f"{average_price:.2f}"
            else:
                context['average'] = 0
            context['chalans'] = my_chalan_for_individual_product

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
        if not self.request.user.role == '':
            my_sales_for_individual_product = SellProduct.objects.filter(
                seller=self.request.user, product=self.id)

            average_price = SellProduct.objects.filter(
                seller=self.request.user, product=self.id).aggregate(Avg('price'))['price__avg']

            user_product_total_quantity = Chalan.objects.filter(
                owner=self.request.user, product=self.id).exclude(customs_clearance_no=None).aggregate(Sum('quantity'))['quantity__sum']

            user_total_sell_product_quantity = SellProduct.objects.filter(
                seller=self.request.user, product=self.id).aggregate(Sum('quantity'))['quantity__sum']

            if user_total_sell_product_quantity == None:
                user_total_sell_product_quantity = 0

            if user_product_total_quantity == None:
                user_product_total_quantity = 0

            if SellProduct.objects.filter(seller=self.request.user, product=self.id).exists():
                unit_for_chalan = SellProduct.objects.filter(
                    seller=self.request.user, product=self.id).values('unit').first()['unit']
                context['unit'] = unit_for_chalan
            else:
                context['message'] = "NO SELL IS RECORDED FOR THIS PRODUCT"

            context['product_name'] = Product.objects.filter(
                id=self.kwargs['pro_id']).values('name').first()['name']
            context['product'] = Product.objects.filter(
                id=self.kwargs['pro_id']).first()
            context['total'] = user_product_total_quantity
            context['sold'] = user_total_sell_product_quantity
            context['available'] = (
                user_product_total_quantity - user_total_sell_product_quantity)
            context['average'] = average_price
            context['sales'] = my_sales_for_individual_product



# IF USER IS ADMIN
        else:
            my_sales_for_individual_product = SellProduct.objects.filter(
                product=self.id)

            average_price = SellProduct.objects.filter(
                product=self.id).aggregate(Avg('price'))['price__avg']

            user_product_total_quantity = Chalan.objects.filter(
                product=self.id).exclude(customs_clearance_no=None).aggregate(Sum('quantity'))['quantity__sum']

            user_total_sell_product_quantity = SellProduct.objects.filter(
                product=self.id).aggregate(Sum('quantity'))['quantity__sum']

            if user_total_sell_product_quantity == None:
                available = user_product_total_quantity - 0
            else:
                available = user_product_total_quantity - user_total_sell_product_quantity

            if SellProduct.objects.filter(product=self.id).exists():
                unit_for_chalan = SellProduct.objects.filter(
                    product=self.id).values('unit').first()['unit']
                context['unit'] = unit_for_chalan
            else:
                context['message'] = "NO SELL IS RECORDED FOR THIS PRODUCT"

            context['product_name'] = Product.objects.filter(
                id=self.kwargs['pro_id']).values('name').first()['name']
            context['product'] = Product.objects.filter(
                id=self.kwargs['pro_id']).first()
            context['total'] = user_product_total_quantity
            context['sold'] = user_total_sell_product_quantity
            context['available'] = available
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
    # print("HELLLLLLLLLLLLLLLLO")
    # print(obj.pending)
    obj.pending = False
    obj.save(update_fields=["pending"])

    @receiver(post_save, sender=SellProduct)
    def create_object(sender, instance, created, **kwargs):
        user = User.objects.get(trade_license_no=instance.buyer)
        # print(user)
        if created and instance.pending == False:
            Chalan.objects.create(owner=user, product=instance.product, quantity=instance.quantity,
                                  unit=instance.unit, price=instance.price, import_date=instance.sell_date,
                                  imported_from=instance.seller.username)
            post_save.connect(create_object, sender=SellProduct)

    create_object(sender=SellProduct, instance=obj, created=True)
    return HttpResponse("Done")




#TO SEE THE DIFFERENCE BETWEEN WHOLESALE MARKET AND LOCAL MARKET
class DifferenceBetweenWholeSaleRetailerMarketView(ListView):
    model = SellProduct
    # USE THE TEMPLATE You want to render
    template_name = 'lenden/difference_showing_page.html'
    context_object_name = 'chalans'
    paginate_by = 3

    def get_queryset(self):
        self.id = get_object_or_404(Product, id=self.kwargs['pro_id'])
        return Product.objects.filter(id=self.request.user.id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # CALCULATE AVAILABILITY Of Product In market.

        product_total_quantity_to_importers = Chalan.objects.filter(
                    product=self.id,owner__role='importer').exclude(customs_clearance_no=None).aggregate(Sum('quantity'))['quantity__sum']
        sold_product_quantity_to_wholesellers = Chalan.objects.filter(
                    product=self.id,owner__role='wholeseller').aggregate(Sum('quantity'))['quantity__sum']

        if product_total_quantity_to_importers == None:
            product_total_quantity_to_importers = 0
        if sold_product_quantity_to_wholesellers == None:
            sold_product_quantity_to_wholesellers = 0

        available_in_importer_to_wholeseller_market = product_total_quantity_to_importers - sold_product_quantity_to_wholesellers
        print(sold_product_quantity_to_wholesellers)
        print(available_in_importer_to_wholeseller_market)


        # CALCULATE AVAILABILITY Of Product In Wholesaler Market.

        product_total_quantity_to_wholesellers = Chalan.objects.filter(
                    product=self.id,owner__role='wholeseller').aggregate(Sum('quantity'))['quantity__sum']
        sold_product_quantity_to_retailers = Chalan.objects.filter(
                    product=self.id,owner__role='retailer').aggregate(Sum('quantity'))['quantity__sum']

        if product_total_quantity_to_wholesellers == None:
            product_total_quantity_to_wholesellers = 0
        if sold_product_quantity_to_retailers == None:
            sold_product_quantity_to_retailers = 0

        available_in_wholeseller_to_retailer_market = product_total_quantity_to_wholesellers - sold_product_quantity_to_retailers

        print(available_in_wholeseller_to_retailer_market)



        # CALCULATING TODAY's Average_price in Importer to wholesaler market
        average_price_in_importer_to_wholeseller = SellProduct.objects.filter(
                product=self.id, seller__role = 'importer',pending=False,sell_date__gte=datetime.date.today()).aggregate(Avg('price'))['price__avg']
        # CALCULATING TODAY's Average_price in Wholesaller to retailer market
        average_price_in_wholeseller_to_retailer = SellProduct.objects.filter(
                product=self.id, seller__role = 'wholeseller',pending=False,sell_date__gte=datetime.date.today()).aggregate(Avg('price'))['price__avg']

        if average_price_in_importer_to_wholeseller == None:
            average_price_in_importer_to_wholeseller = 0
        if average_price_in_wholeseller_to_retailer == None:
            average_price_in_wholeseller_to_retailer = 0
        


        # print(average_price_in_importer_to_wholeseller)
        # print(average_price_in_wholeseller_to_retailer)

        # print("Difference = ", average_price_in_wholeseller_to_retailer-average_price_in_importer_to_wholeseller)

        context['avg_in_imp_to_whlSale'] = average_price_in_importer_to_wholeseller
        context['avg_in_whlSale_to_rtlr'] = average_price_in_wholeseller_to_retailer
        context['difference'] = average_price_in_wholeseller_to_retailer-average_price_in_importer_to_wholeseller

        context['total_product_to_importers'] = product_total_quantity_to_importers
        context['sold_to_wholesellers'] = sold_product_quantity_to_wholesellers
        context['available_in_importer_to_wholeseller_marktet'] = available_in_importer_to_wholeseller_market

        context['total_product_to_wholesellers'] = product_total_quantity_to_wholesellers
        context['sold_to_retailers'] = sold_product_quantity_to_retailers
        context['available_in_wholeseller_to_importer_marktet'] = available_in_wholeseller_to_retailer_market

        return context





#PENDING BUYING RECORDS

class PendingBuyingRecodrs(ListView):
    model = SellProduct
    # USE THE TEMPLATE You want to render
    template_name = 'lenden/sale_product_details.html'
    context_object_name = 'chalans'
    paginate_by = 3

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pending_records = SellProduct.objects.filter(buyer= self.request.user.trade_license_no,pending=True)
        print(pending_records)
        context['pending_records'] = pending_records
        return context




# DJANGO NOTIFICATION MARK AS READ
from notifications.models import Notification
def mark_as_read(request):
    url = request.META.get("HTTP_REFERER")  # get last url
    unread_notifications = Notification.objects.filter(recipient= request.user, unread=True)
    print(unread_notifications)
    for notification in unread_notifications:
        notification.unread = False
        notification.save()
        print(notification)

    return redirect(url)



