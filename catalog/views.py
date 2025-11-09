from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from catalog.models import Product


class ContactsView(View):
    """View для страницы контактов"""

    def get(self, request, *args, **kwargs):
        return render(request, "catalog/contacts.html")

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")


class ProductsListView(ListView):
    """View для списка продуктов"""

    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """View для детальной страницы продукта"""

    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'products'

# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
#     return render(request, "contacts.html")

# def products_list(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, 'products_list.html', context)

# def product_detail(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     context = {"product": product}
#     return render(request, 'product_detail.html', context)