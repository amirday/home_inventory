from django.contrib import admin
from django.urls import path
from .views import (Index, SignUpView, Dashboard, AddItem, EditItem, 
                    EmptyItem, DeleteItem, ShoppingList, FullfilItem)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('shopping_list/<str:category>/', ShoppingList.as_view(), name='shopping_list'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('fullfil-item/<int:pk>/', FullfilItem.as_view(), name='fullfil-item'),
    path('empty-item/<int:pk>/', EmptyItem.as_view(), name='empty-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
]