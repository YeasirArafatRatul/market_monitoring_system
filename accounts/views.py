from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages, auth
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, UpdateView, ListView, FormView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from accounts.models import User
from .forms import *
from .forms import ProfileUpdateForm, UserUpdateForm
from lenden.models import Product
from lenden.forms import *
from django.db.models import Count, Max


@login_required(login_url='/login')
def home(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    product_from_chalan = Chalan.objects.filter(
        owner=current_user)

    unique_products = Chalan.objects.filter(owner=current_user).order_by(
        'product').values('product').distinct()

    print(unique_products)
    products = []

    for k in unique_products:
        query = Product.objects.get(id=k['product'])
        products.append(query)

    print(products)

    chalans = Chalan.objects.filter(
        owner_id=request.user.id).order_by('-id')[:8]
    pending_sale_record_of_buyer = SellProduct.objects.filter(
        buyer=current_user.trade_license_no, pending=True).order_by('-created_at').count()

    # print(current_user.trade_license_no)

    pending_sale_record_of_seller = SellProduct.objects.filter(
        seller=current_user, pending=True).order_by('-created_at').count()

    total_sales = SellProduct.objects.filter(
        seller=current_user).aggregate(Sum('price'))['price__sum']

    if total_sales == None:
        total_sales = 0

    number_of_sellings = SellProduct.objects.filter(
        seller=current_user).count()

    number_of_buyings = SellProduct.objects.filter(
        buyer=current_user.trade_license_no).count()

    if number_of_buyings == None:
        number_of_buyings = 0
    elif number_of_sellings == None:
        number_of_sellings = 0

    number_of_transactions = number_of_buyings + number_of_sellings
# User UPDATE FORM
    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        product_form = AddChalanForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, "Your Profile is updated successfully")
            return redirect('accounts:home')

        if product_form.is_valid():
            product_form.instance.owner = request.user
            product_form.save()
            print('____________________I AM SAVED_________________')
            messages.success(
                request, "New Product is Added")
            return redirect('accounts:home')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        product_form = AddChalanForm(
            request.POST)

    context = {
        'user': current_user,
        'chalans': chalans,
        'user_form': user_form,
        'profile_form': profile_form,
        'product_form': product_form,
        'pending_sale_record_of_buyer': pending_sale_record_of_buyer,
        'pending_sale_record_of_seller': pending_sale_record_of_seller,
        'total_sales': total_sales,
        'number_of_transactions': number_of_transactions,
        'products': products,
    }

    return render(request, 'dashboard/index.html', context)


# class HomeView(FormView, ListView):
#     model = User
#     template_name = 'dashboard/dashboard.html'
#     context_object_name = 'user'

#     def post(self, request, *args, **kwargs):
#         if self.request.method == "POST":
#             user_form = UserUpdateForm(
#                 self.request.POST, instance=self.request.user)
#             profile_form = ProfileUpdateForm(
#                 self.request.POST, self.request.FILES, instance=self.request.user.userprofile)

#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(
#                     self.request, "Your Profile is updated successfully")
#             return redirect('accounts:home')
#         else:
#             user_form = UserUpdateForm(instance=self.request.user)
#             profile_form = ProfileUpdateForm(
#                 instance=self.request.user.userprofile)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.filter(
#             owner_id=self.request.user.id).order_by('-id')[:8]
#         context['user_form'] = UserUpdateForm(instance=self.request.user)
#         context['profile_form'] = ProfileUpdateForm(
#             instance=self.request.user.userprofile)
#         return context


# Create your views here.
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = 'home'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, 'You Are Already Locked in an account')
            # return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/register.html', {'form': form})


# ---------------------------------------------------------------
#  LOGIN - LOGOUT
# ---------------------------------------------------------------

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')
    success_message = "Welcome To Market Monitoring System"


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = reverse_lazy('accounts:home')
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # return redirect('accounts:home')
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        print("Logged In Sucessfully")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


@ login_required(login_url='/login')
def profile(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {
        'profile': profile,
    }
    return render(request, 'accounts/demo_profile.html', context)


@ login_required(login_url='/login')
def user_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, "Your Profile is updated successfully")
            return redirect('accounts:home')
    else:

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {

        'user_form': user_form,
        'profile_form': profile_form,


    }

    return render(request, 'accounts/user_update.html', context)


@login_required(login_url='/login')  # Check login
def password_change(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('accounts:home')
        else:
            return render(request, 'accounts/password_change.html', {'form': form})
            # messages.error(
            #     request, 'Error' + str(form.errors))
            # return HttpResponseRedirect(url)
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password_change.html', {'form': form
                                                                 })


class ListOfUsersView(ListView):
    model = User
    template_name = 'accounts/users.html'
    context_object_name = 'users'
    paginate_by = 1

    def get_queryset(self):
        self.role = self.kwargs['role']
        return self.model.objects.filter(role=self.role)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['role'] = self.kwargs['role'].capitalize()+'s'
        return context
