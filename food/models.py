from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import  RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=100)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE) #self yani kendiyle ilişki
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="75"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug}) #otomatik slug için

class Restaurant(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE) #Category modeli ile ilişkili
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    #image = models.ImageField(blank=True, upload_to='images/')
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="75"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug}) #otomatik slug için


class food(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #Category modeli ile ilişkili
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True,max_length=255)
    description = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField() #miktar
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="75"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def catimg_tag(self):
        return mark_safe((Category.status))

    def get_absolute_url(self):
        return reverse('food_detail', kwargs={'slug': self.slug})



class Images(models.Model):
    Food = models.ForeignKey(food, on_delete=models.CASCADE) #food ile image ilişkilendirildi
    title = models.CharField(max_length=50, blank=True) #ondelete models Cascade eğer food u silersen image i de silinsin
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self): #ImagesObject adı ile gözükmemesi için
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    Food = models.ForeignKey(food,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField( max_length=50)
    comment = models.CharField(blank=True, max_length=200)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rate'] #bu alanlar html de çağırılacak

