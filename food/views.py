from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from food.models import CommentForm, Comment


def index(request):
    return HttpResponse("Food Page");

@login_required(login_url='/login') #login kontrolü
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST': #form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():#form dan 3 eleman geldi mi kontrol
            current_user=request.user #access user session information

            data = Comment() #model ile bağlantı kur
            data.user_id=current_user.id
            data.Food_id=id
            data.subject=form.cleaned_data['subject'] #bu 3 ü formdan alındı
            data.comment=form.cleaned_data['comment']
            data.rate=form.cleaned_data['rate']
            data.ip=request.META.get('REMOTE_ADDR') #client computer ip address
            data.save() #veritabanına kaydet
            messages.success(request,"Yorumunuz başarı ile gönderilmiştir. Teşekkürler")

            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz gönderilemedi. Lütfen kontrol ediniz")
    return HttpResponseRedirect(url)
