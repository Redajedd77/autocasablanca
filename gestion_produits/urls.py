# gestion_produits/urls.py
from django.urls import path, include
from .views import produit_list, produit_add, produit_edit, produit_delete, login_view, home, produit_detail
from django.contrib.auth import views as auth_views
from .views import ProduitListAPIView
from .views import avito_car_listings

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('root/', produit_list, name='produit_list'),
    path('', home, name='home'),
    path('produits/<int:produit_id>/', produit_detail, name='produit_detail'),
    path('produits/ajouter/', produit_add, name='produit_add'),
    path('produits/<int:pk>/modifier/', produit_edit, name='produit_edit'),
    path('produits/<int:pk>/supprimer/', produit_delete, name='produit_delete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/produits/', ProduitListAPIView.as_view(), name='produit_list_api'),
     path('list/', avito_car_listings, name='avito_car_listings'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

