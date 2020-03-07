from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    is_fisherman = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=False)


class Fisherman(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    First_Name = models.CharField(max_length=200,  null=True)
    Last_Name = models.CharField(max_length=200,  null=True)
    Mobile_No = models.CharField(null=True, max_length=10, validators=[
                                 RegexValidator(r'^\d{1,10}$')])
    Region = models.CharField(max_length=500,  null=True)

    def __str__(self):
        return self.user.username

    class Meta:
    	verbose_name_plural = "Fishermen"


class Retailer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    First_Name = models.CharField(max_length=200,  null=True)
    Last_Name = models.CharField(max_length=200,  null=True)
    Mobile_No = models.CharField(null=True, max_length=10, validators=[
                                 RegexValidator(r'^\d{1,10}$')])
    Address = models.CharField(max_length=500,  null=True)

    def __str__(self):
        return self.user.username


class Fish(models.Model):
    name = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

    class Meta:
    	verbose_name_plural = "Fish"


class Retailer_Inventory(models.Model):
    Retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    Fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def __str__(self):
        return self.Retailer.user.username

    class Meta:
    	verbose_name_plural = "Retailer Inventories"
  

