from django.contrib import admin

# Register your models here.
from order.models import ShopCart


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','Food','price','quantity','amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)