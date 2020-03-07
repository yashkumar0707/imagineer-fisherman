"""fisherman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import SignUpView, RetailerSignUpView, FishermanSignUpView, retailerinventory
from . import views

app_name = "main"

urlpatterns = [
    path('', SignUpView.as_view(), name="signup"),
    path('register/fisherman/', FishermanSignUpView.as_view(),
         name='fisherman_signup'),
    path('register/retailer/', RetailerSignUpView.as_view(), name='retailer_signup'),
    path('login/', views.login_request, name='login'),

    path('logout/', views.logout_request, name='logout'),
    #path('fisherhome', views.fisherhome, name='fisherhome'),
    #path('retailerhome', views.retailerhome, name='retailerhome')
    path('fisherhome/', views.fisherhome, name='fisherhome'),
    path('retailerhome/', retailerinventory.as_view(), name='retailerhome'),
]
