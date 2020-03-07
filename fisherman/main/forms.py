from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User

 

from django.db import transaction

from .models import Fisherman, User, Retailer

class FishermanSignUpForm(UserCreationForm):
    First_Name = forms.CharField(max_length=100, required=True)
    Last_Name = forms.CharField(max_length=100, required=True)
    Region = forms.CharField(max_length=100, required=True)
    Mobile_No = forms.CharField(max_length = 10,required = True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("First_Name","Last_Name", "Region", "Mobile_No", "username", "password1", "password2")

    @transaction.atomic
    def save(self, commit = True):
        user = super().save(commit=False)
        user.is_fisherman = True
        user.save()
        fisherman = Fisherman.objects.create(user=user)
        fisherman.First_Name = self.cleaned_data.get('First_Name')
        fisherman.Last_Name =self.cleaned_data.get('Last_Name')
        fisherman.Region =self.cleaned_data.get('Address')
        fisherman.Mobile_No =self.cleaned_data.get('Mobile_No')
        fisherman.save()
        return user

class RetailerSignUpForm(UserCreationForm):
    First_Name = forms.CharField(max_length=100, required=True)
    Last_Name = forms.CharField(max_length=100, required=True)
    Address = forms.CharField(max_length=100, required=True)
    Mobile_No = forms.CharField(max_length = 10,required = True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("First_Name","Last_Name", "Address", "Mobile_No", "username", "password1", "password2")

    @transaction.atomic
    def save(self, commit = True):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()
        owner = Retailer.objects.create(user=user)
        owner.First_Name = self.cleaned_data.get('First_Name')
        owner.Last_Name =self.cleaned_data.get('Last_Name')
        owner.Age =self.cleaned_data.get('Age')
        owner.Gender=self.cleaned_data.get('Gender')
        owner.Address =self.cleaned_data.get('Address')
        owner.Mobile_No =self.cleaned_data.get('Mobile_No')
        owner.save()
        return user



