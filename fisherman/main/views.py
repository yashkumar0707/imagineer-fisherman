from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView, DeleteView
from .models import Fisherman, Retailer, User
from .forms import FishermanSignUpForm, RetailerSignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout,authenticate





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
            user = authenticate(username = username,password =password)
            if user is not None:
                login(request,user)
                #messages.info(request, f'Logged in as : {username}')
                return redirect("main:signup")
            else:
                messages.error(request, "Invalid Username or Password")
        else:
            messages.error(request, "Invalid Username or Password")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form":form})