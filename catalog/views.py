from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product

# Create your views here.


# def home(request):
#     return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, "contacts.html")


def products_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'products_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = {"product": product}
    return render(request, 'product_detail.html', context)