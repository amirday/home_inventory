from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from home_inventory.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import F


class FullfilItem(View):
	def post(self, request, *args, **kwargs):
		item = get_object_or_404(InventoryItem, id=self.kwargs['pk'])
		item.quantity = item.desired_quantity
		item.save()
		return HttpResponse(status=204)


class EmptyItem(View):
    def post(self, request, *args, **kwargs):
        item = get_object_or_404(InventoryItem, id=self.kwargs['pk'])
        item.quantity = 0
        item.save()
        return HttpResponse(status=204)
	
class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')
        return render(request, 'inventory/index.html')


class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.filter(user=self.request.user.id).annotate(
					quantity_difference=-F('desired_quantity') + F('quantity')
        ).order_by('quantity_difference')		
		
		all_categories = Category.objects.all()
		low_inventory_ids = InventoryItem.objects.filter(
								user=request.user.id,
								quantity__lt=F('desired_quantity')
							).values_list('id', flat=True)
		
		return render(request, 'inventory/dashboard.html', {'items': items, 
													  'low_inventory_ids': low_inventory_ids, 
													  'all_categories': all_categories,
													  'is_shopping_list': False})

class ShoppingList(LoginRequiredMixin, View):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = self.kwargs['category']
		return context

	def get(self, request, *args, **kwargs):
		self.category = kwargs.get('category', None)
		# Get all items with quantity less than desired quantity
		items = InventoryItem.objects.filter(category__name=self.category).filter(
			user=request.user.id,
			quantity__lt=F('desired_quantity')
		).order_by('id')
		return render(request, 'inventory/dashboard.html', {'items': items, 
										'low_inventory_ids': [], 
										'is_shopping_list': True})

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['item_names'] = InventoryItem.objects.values_list('name', flat=True)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_initial(self):
		initial = super().get_initial()
		initial['name'] = self.request.GET.get('name', '')
		return initial

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'