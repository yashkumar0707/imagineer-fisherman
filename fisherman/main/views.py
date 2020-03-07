from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import Fisherman, Retailer, User
from .forms import FishermanSignUpForm, RetailerSignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




# Create your views here.


class SignUpView(TemplateView):
    template_name = 'main/base.html'

class FishermanSignUpView(CreateView):
    model = User
    form_class = FishermanSignUpForm
    template_name = 'main/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'fisherman'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')

class RetailerSignUpView(CreateView):
    model = User
    form_class = RetailerSignUpForm
    template_name = 'main/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'retailer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:homepage')