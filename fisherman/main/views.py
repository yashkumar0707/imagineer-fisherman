from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import Fisherman, Retailer, User, Retailer_Inventory
from .forms import FishermanSignUpForm, RetailerSignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate


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
        return redirect('main:signup')


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
        return redirect('main:signup')


"""def logout_request(request):
    logout(request)
    messages.info(request,"Logged Out Successfully")
    return redirect("main:homepage")"""


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
        return redirect('main:fisherhome')
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
