# gestion_produits/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
# gestion_produits/views.py
from django.contrib.auth.decorators import user_passes_test
# gestion_produits/views.py
from .forms import ProduitForm

from django.db.models import Q

# gestion_produits/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Produit
from .serializers import ProduitSerializer
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# views.py
from django.core.paginator import Paginator






def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('produit_list')  # Redirige vers la page des produits après login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)




@superuser_required
def avito_car_listings(request):
    url = 'https://www.avito.ma/fr/maroc/voitures_d_occasion-à_vendre?has_price=true'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    cars = soup.find_all('div', class_='listing-container')

    car_listings = []
    for car in cars:
        title = car.find('h2').text.strip() if car.find('h2') else "N/A"
        price = car.find('span', class_='price').text.strip() if car.find('span', class_='price') else "N/A"
        location = car.find('span', class_='item-location').text.strip() if car.find('span', class_='item-location') else "N/A"

        car_listings.append({
            'title': title,
            'price': price,
            'location': location,
        })

    return render(request, 'avito_car_listings.html', {'car_listings': car_listings})



class ProduitListAPIView(APIView):
    def get(self, request):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)



def home(request):
    search_query = request.GET.get('q', '')  # Get search query from the request
    products = Produit.objects.filter(nom__icontains=search_query)  # Filter products by name

    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'search_query': search_query})




def produit_detail(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    return render(request, 'produit_detail.html', {'produit': produit})





@superuser_required
def produit_list(request):
    query = request.GET.get('q')  # Get the search query from the URL
    if query:
        produits = Produit.objects.filter(
            Q(nom__icontains=query) |  # Search by name (case-insensitive)
            Q(description__icontains=query)  # Search by description (add more fields if needed)
        )
    else:
        produits = Produit.objects.all()  # No search query, display all products
    return render(request, 'produit_list.html', {'produits': produits, 'query': query})





@superuser_required
def produit_add(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm()
    return render(request, 'produit_form.html', {'form': form})

@superuser_required
def produit_edit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('produit_list')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'product_form1.html', {'form': form, 'action': 'Modifier'})
@superuser_required
def produit_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        return redirect('produit_list')
    return render(request, 'produit_confirm_delete.html', {'produit': produit})

