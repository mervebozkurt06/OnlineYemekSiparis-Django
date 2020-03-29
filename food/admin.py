from django.contrib import admin

# Register your models here.
from food.models import Category, food, Images

class FoodImageInLine(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']


class foodAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','image','amount', 'status']
    list_filter = ['status','category']
    inlines = [FoodImageInLine]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'food', 'image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Category,CategoryAdmin)
admin.site.register(food,foodAdmin)
admin.site.register(Images,ImagesAdmin)



