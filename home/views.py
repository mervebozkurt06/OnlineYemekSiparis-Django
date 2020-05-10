from unicodedata import category

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render


# Create your views here.
from food.models import food, Category, Images, Comment
from home.forms import SearchForm
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
    context = {'setting': setting, 'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
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
    #form=ContactFormu()
    context = {'setting': setting}
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
            foods = food.objects.filter(title__icontains=query) #Select * form product where title like %query%
            context = {'foods':foods,
                       'category':category,
                       }
            return render(request,'foods_search.html',context)

    return HttpResponseRedirect('/')