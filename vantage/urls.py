# vantage/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_produits.urls')),  # Inclure les URLs de ton application
]
