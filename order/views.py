from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from food.models import Category, food
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderFood


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
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() #sepetteki ürünlerin sayısı alındı
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
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() #sepetteki ürünlerin sayısı alındı
        messages.success(request, "Ürün başarı ile sepete eklenmiştir. Teşekkür ederiz")
        return HttpResponseRedirect(url)

    messages.warning(request, "Ürün sepete eklenemedi. Lütfen kontrol ediniz")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # sepetteki ürünlerin sayısı alındı

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
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # sepetteki ürünlerin sayısı alındı
    messages.success(request, "Ürün sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")

@login_required(login_url='/login')
def orderfood(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in schopcart:
        total += rs.Food.price * rs.quantity #toplamı hesapla

    if request.method == 'POST': #form post edildiyse food_detail dan
        form = OrderForm(request.POST)
        if form.is_valid(): #geçerli mi csrf kontrolü
            #kredi kartı bilgilerini bankaya gönder onay gelirse devam et
            #....if kontrolü....
            data = Order() #order tablosu ile ilişki kur
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper() # random kod üretir
            data.code = ordercode
            data.save()

            #sepetteki ürünleri order'a kaydetmek için aşağıdaki kodlar
            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in schopcart:
                detail = OrderFood()
                detail.order_id = data.user_id
                detail.Food_id = rs.Food_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity

                Food = food.objects.get(id=rs.Food_id)
                Food.amount -= rs.quantity #ürün stoktan düşme
                Food.save()

                detail.price = rs.Food.price
                detail.amount = rs.amount
                detail.save()

            ShopCart.objects.filter(user_id=current_user.id).delete() #sepet temizlendi
            request.session['cart_items']=0
            messages.success(request, "Your order has been completed. Thank you")
            return render(request,'Order_Completed.html',{'ordercode':ordercode,'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderfood")

    #post yoksa
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'schopcart': schopcart,
                'category': category,
                'total': total,
                'form': form,
                'profile': profile,
                }
    return render(request,'Order_Form.html',context)



