from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import *
# Create your views here.
class AddEducationView(LoginRequiredMixin, CreateView):
    form_class = AddProductForm
    template_name = 'accounts/add_education.html'
    success_url = reverse_lazy('accounts:my-profile')

    def form_valid(self, form):
        request = self.request
        form.instance.owner = self.request.owner
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

