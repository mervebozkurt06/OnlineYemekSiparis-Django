import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render


# Create your views here.
from food.models import food, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = food.objects.all()[:4]
    category = Category.objects.all()
    dayfoods = food.objects.all()[:4]
    lastfoods = food.objects.all().order_by('-id')[:4]
    randomfoods = food.objects.all().order_by('?')[:4]

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
               'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category
               }
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == 'POST':  # form post ediliyor
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name'] #formdan bilgi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)  #post edilmezse bura çalışır
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
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] # formdan bilgiyi al
            catid = form.cleaned_data['catid']#sonradan eklendi
            if catid==0:#sonradan eklendi
                foods = food.objects.filter(title__icontains=query)#sonradan eklendi
            else:#sonradan eklendi
                foods = food.objects.filter(title__icontains=query,category_id=catid)#sonradan eklendi

            #foods = food.objects.filter(title__icontains=query) #Select * form product where title like %query%
            context = {'foods':foods,
                       'category':category,
                       }
            return render(request,'foods_search.html',context)

    return HttpResponseRedirect('/')

def food_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        Food = food.objects.filter(title__icontains=q)
        results = []
        for rs in Food:
            food_json = {}
            food_json = rs.title
            results.append(food_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

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
            return HttpResponseRedirect('/')


    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)


