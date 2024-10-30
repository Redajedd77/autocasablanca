# gestion_produits/serializers.py
from rest_framework import serializers
from .models import Produit

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'  # Include all fields of the Produit model
