from django.urls import path, include
from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductsListView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", ProductsListView.as_view(), name="product_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
]
