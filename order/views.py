from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile
from food.models import Category
from order.models import ShopCartForm, ShopCart


def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login') #check login
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user

    #*******ürün sepette var mı kontrolü*******
    checkfood = ShopCart.objects.filter(Food_id=id)
    if checkfood:
        control = 1 #ürün sepette var
    else:
        control = 0 #ürün sepette yok

    if request.method == 'POST': #form post edildiyse food_detail dan
        form = ShopCartForm(request.POST)
        if form.is_valid(): #geçerli mi csrf kontrolü
            if control == 1: #ürün varsa güncelle
                data = ShopCart.objects.get(Food_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else: #ürün yoksa ekle
                data = ShopCart()  # model ile bağlantı kur
                data.user_id = current_user.id
                data.Food_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür ederiz")
        return HttpResponseRedirect(url)

    else: #ürün direk sepete ekle ile geldiyse
        if control == 1:  # ürün varsa güncelle
            data = ShopCart.objects.get(Food_id=id)
            data.quantity += 1
            data.save()
        else: #ürün yoksa ekle
            data = ShopCart() #model ile bağlantı kur
            data.user_id = current_user.id
            data.Food_id = id
            data.quantity = 1
            data.save() #veritabanına kaydet
        messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür ederiz")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürün sepete eklenemedi. Lütfen kontrol ediniz")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in schopcart:
        total += rs.Food.price * rs.quantity

    context = {'schopcart': schopcart,
               'category': category,
               'total': total,
               }
    return render(request, 'Shopcart_foods.html',context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")
