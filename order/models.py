from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from food.models import food


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Food = models.ForeignKey(food, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.Food.title

    @property
    def amount(self):
        if self.Food_id is None:
            return None
        return self.quantity * self.Food.price

    @property
    def price(self):
        if self.Food_id is not None:
           return self.Food.price

class ShopCartForm(ModelForm): #kaç adet olacak
    class Meta:
        model = ShopCart
        fields = ['quantity']