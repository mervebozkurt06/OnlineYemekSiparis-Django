from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from food.models import Category, food, Images #modelden Category food ve Images eklendi

class FoodImageInLine(admin.TabularInline): #5 li foto eklemek icin
    model = Images #Image tablosu
    extra = 5

class CategoryAdmin(admin.ModelAdmin): #admindeki categories in görüntüsü
    list_display = ['title', 'status','image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class foodAdmin(admin.ModelAdmin): #admindeki foods tablosu
    list_display = ['title','category','price','amount', 'image_tag', 'status']
    list_filter = ['status','category']
    inlines = [FoodImageInLine] #aşağıdaki 5 resmi eklemek için
    readonly_fields = ('image_tag',) # image ların resim olarak görünmesi için


class ImagesAdmin(admin.ModelAdmin): #Imagess tablosu admindeki
    list_display = ['title', 'food', 'image_tag']
    readonly_fields = ('image_tag',)

class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions',
                    'indented_title',
                    'related_products_count',
                    'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    list_filter = ['status']


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                food,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 food ,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(Category,CategoryAdmin) #admin de tablo gösterilmesi
admin.site.register(food,foodAdmin)
admin.site.register(Images,ImagesAdmin)



