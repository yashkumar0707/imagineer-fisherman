from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import Fisherman, Retailer, User, Retailer_Inventory, Sales
from .forms import FishermanSignUpForm, RetailerSignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os.path
import openpyxl
import pandas as pd
from fbprophet import Prophet
from django_pandas.io import read_frame

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
        return redirect('main:fisherhome')


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
        return redirect('main:retailerhome')


class RetailerInventoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Retailer_Inventory
    login_url = '/login/'
    fields = ["qty"]
    template_name = 'main/update.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'inventory'
    success_url = '/retailerhome'

    def form_valid(self, form):
        form.instance.Retailer = self.request.user.retailer
        return super().form_valid(form)

    def test_func(self):
        car = self.get_object()
        if self.request.user.retailer == car.Retailer:
            return True
        return False


def logout_request(request):
    logout(request)
    messages.info(request, "Logged Out Successfully")
    return redirect("main:signup")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('qwer')
                """if user.is_fisherman:
                    type_obj = Fisherman.objects.get(user=user)
                else:
                    type_obj = Retailer.objects.get()"""
                if user.is_authenticated and user.is_fisherman:
                    print('uiui')
                    return redirect('main:fisherhome')  # Go to student home
                if user.is_authenticated and user.is_retailer:
                    print('yash')
                    return redirect('main:retailerhome')  # Go to teacher home

            else:
                messages.error(request, "Invalid Username or Password")
        else:
            messages.error(request, "Invalid Username or Password")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form})


def fisherhome(request):
    if request.user.is_authenticated and request.user.is_fisherman:
        qs = Sales.objects.all()
        df = read_frame(qs, fieldnames=['ds', 'y'])
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=10)
        forecast = m.predict(future)
        print(forecast[['ds', 'yhat']].iloc[:1])
        ans = forecast[['ds', 'yhat']].iloc[:1]
        return render(request, "main/fisherman_home.html", {'ans': ans})
    elif request.user.is_authenticated and request.user.is_retailer:
        return redirect('main:retailerhome')
    else:
        return redirect('main:login')


def retailerhome(request):
    if request.user.is_authenticated and request.user.is_retailer:
        return redirect('main:retailerhome')
    elif request.user.is_authenticated and request.user.is_fisherman:
        return redirect('main:fisherhome')
    else:
        return redirect('main:login')


class retailerinventory(ListView):
    model = Retailer_Inventory
    template_name = "main/retailer_home.html"
    context_object_name = 'inventory'
    ordering = ['-qty']
