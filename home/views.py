import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render


# Create your views here.
from food.models import food, Category, Images, Comment, Restaurant
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from order.models import ShopCart


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = food.objects.all()[:4]
    category = Category.objects.all()
    dayfoods = food.objects.all()[:4]
    lastfoods = food.objects.all().order_by('-id')[:4]
    randomfoods = food.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # sepetteki ürünlerin sayısı alındı

    context = {'setting': setting,
               'category': category,
               'page':'home',
               'sliderdata':sliderdata,
               'dayfoods':dayfoods,
               'lastfoods':lastfoods,
               'randomfoods':randomfoods
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'category': category,
               'setting': setting,
               'page':'hakkimizda'
               }
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST':  # form post ediliyorsa
        form = ContactFormu(request.POST) #sitede gösterilen ContactFormundaki verileri forma al
        if form.is_valid(): #form validse yani bilgiler doğru girilmişse
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name'] #formdan bilgi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)  #post edilmediyse bu sayfada bunu çalıştır(bilgi için contactus)
    form=ContactFormu()
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category}
    return render(request, 'iletisim.html', context)

def category_foods(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    foods = food.objects.filter(category_id=id)
    context = {'foods': foods,
               'category': category,
               'categorydata': categorydata
               }
    return render(request,'foods.html',context)

def food_detail(request,id,slug):
    category = Category.objects.all()
    Food = food.objects.get(pk=id)
    images = Images.objects.filter(Food_id=id)
    comments=Comment.objects.filter(Food_id=id,status='True')
    context = {'Food': Food,
               'category': category,
               'images': images,
               'comments':comments,
               }
    return render(request,'food_detail.html',context)

def food_search(request):
    if request.method == 'POST': #post edildi mi
        form = SearchForm(request.POST) #searchform unu çağırıp validmi bak
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] # formdan bilgiyi al
            foods = food.objects.filter(title__icontains=query) #Select * form product where title like %query%
            context = {'foods':foods,
                       'category':category,
                       }
            return render(request,'foods_search.html',context)

    return HttpResponseRedirect('/')



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası! | Kullanıcı adı yada şifre yanlış ")
            return HttpResponseRedirect('/login')


    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            #userı ekleyip login ettikten sonra
            #kullanıcı profilini güncellemek isterse
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/usern.png"
            data.save()
            messages.success(request, "Hoşgeldiniz.. Sitemize başarılı bir şekilde kayıt oldunuz.")
            return HttpResponseRedirect('/')


    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context={
        'category': category,
        'faq': faq,
    }

    return render(request, 'faq.html',context)