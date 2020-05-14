from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderFood, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','Food','price','quantity','amount']
    list_filter = ['user']


class OrderFoodline(admin.TabularInline):
    model = OrderFood
    readonly_fields = ('user','Food','price','quantity','amount')
    can_delete = False #değiştirilmesin
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip','last_name','phone','city','total')
    can_delete = False
    inlines = [OrderFoodline] #siparişe ait ürünlerin aynı sayfa da olması için


class OrderFoodAdmin(admin.ModelAdmin):
    list_display = ['user','Food','price','quantity','amount']
    list_filter = ['user']


admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderFood,OrderFoodAdmin)
