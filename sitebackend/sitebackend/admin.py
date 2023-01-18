from django.contrib import admin
from .models import Product

# Registramos el modelo en la administración de Django
admin.site.register(Product)