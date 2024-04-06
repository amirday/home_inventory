from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem, Units


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
	units = forms.ModelChoiceField(queryset=Units.objects.all(), initial=0)
	class Meta:
		model = InventoryItem
		fields = ['name','desired_quantity' ,'quantity', 'units', 'category', 'image']