from django.contrib import admin
from .models import Fisherman, Retailer, Retailer_Inventory, Fish, User, Sales

# Register your models here.
admin.site.register(User)
admin.site.register(Fisherman)
admin.site.register(Retailer)
admin.site.register(Retailer_Inventory)
admin.site.register(Fish)
admin.site.register(Sales)
