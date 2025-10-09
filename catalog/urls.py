from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import contacts, products_list, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", products_list, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>", product_detail, name="product_detail"),
]
