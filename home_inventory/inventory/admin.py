from django.contrib import admin
from .models import InventoryItem, Category, Units

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(Units)