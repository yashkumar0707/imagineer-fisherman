from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import (Fisherman, Retailer, User, Retailer_Inventory, Sales, Fish, Fisherman_Inventory,
                     Retailer_Request)

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
from django.db.models import Sum

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


class FishermanInventoryCreateView(LoginRequiredMixin, CreateView):
    model = Fisherman_Inventory
    login_url = '/login/'
    template_name = 'main/submit_fish.html'
    context_object_name = 'inventory'
    success_url = '/fisherhome'
    fields = ["Fish", "qty"]

    def form_valid(self, form):
        form.instance.Fisherman = self.request.user.fisherman
        return super().form_valid(form)


class RetailerRequestCreateView(LoginRequiredMixin, CreateView):
    model = Retailer_Request
    login_url = '/login/'
    template_name = 'main/request.html'
    context_object_name = 'request'
    success_url = '/fisherhome'
    fields = ["Fish", "qty"]

    def form_valid(self, form):
        form.instance.Retailer = self.request.user.retailer
        return super().form_valid(form)


def inventory(request):
    sums = []
    fishs = []
    for fish in Fish.objects.all():
        temp = Fisherman_Inventory.objects.filter(Fish=fish)
        sum = 0
        for i in temp:
            sum = sum + i.qty
        sums.append([sum, fish.name])
        print(sums)
    return render(request, "inventory.html", context={"sums": sums})


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
        qty = []
        fishn = []
        l = []
        i = 0
        for fish in Fish.objects.all():
            qs = Sales.objects.filter(Fish=fish)
            df = read_frame(qs, fieldnames=['ds', 'y'])
            m = Prophet()
            m.fit(df)
            future = m.make_future_dataframe(periods=10)
            forecast = m.predict(future)
            print(forecast[['ds', 'yhat']].iloc[:1])
            print('njb')
            a1 = forecast[['yhat']].iloc[0]['yhat']
            print(a1)
            qty.append(int(a1))
            a2 = int(a1)
            fishn.append(fish.name)
            l.append([a2, fish.name])
        # ans1 = ans['yhat']
        # print(ans['yhat'])
        for i in range(len(qty)):
            print(qty[i])

        return render(request, "main/fisherman_home.html", {'fishn': fishn, 'qty': qty, 'l': l})
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
