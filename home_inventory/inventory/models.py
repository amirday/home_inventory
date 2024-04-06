from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
	name = models.CharField(max_length=200)
	desired_quantity = models.FloatField()
	quantity = models.FloatField()
	units = models.ForeignKey('Units', on_delete=models.SET_NULL, blank=True, null=True)
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='inventory_images/', blank=True, null=True)


	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

class Units(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'units'

	def __str__(self):
		return self.name