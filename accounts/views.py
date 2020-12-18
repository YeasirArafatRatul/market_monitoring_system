from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages, auth
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, DetailView, UpdateView, ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from accounts.models import User
from .forms import *
from lenden.models import Product


class HomeView(ListView):
    model = User
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # AYUB - Loop Through The 'products' list in template
        context['products'] = Product.objects.filter(owner_id = self.request.user.id).order_by('-id')[:8]
        # print(context)
        return context


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
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)



@login_required(login_url='/login')
def profile(request):

    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)


    context = {
               'profile': profile,
              

               }
    return render(request, 'accounts/demo_profile.html', context)


@login_required(login_url='/login')
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
            return redirect('accounts:profile')
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
            return redirect('accounts:my-profile')
        else:
            return render(request, 'accounts/password_change.html', {'form': form})
            # messages.error(
            #     request, 'Error' + str(form.errors))
            # return HttpResponseRedirect(url)
    else:
        category = JobCategory.objects.all()
        setting = Setting.objects.filter(status=True).first()
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password_change.html', {'form': form, 'categories': category, 'settings': setting,
                                                                 })

