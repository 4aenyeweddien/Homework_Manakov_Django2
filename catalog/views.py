from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from catalog.forms import ProductForm
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
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):
    """View для детальной страницы продукта"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "products"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """View для создания продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """View для редактирования продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.instance
        if 'is_published' in form.changed_data and not product.is_published:
            if not self.request.user.has_perm('catalog.can_unpublish_product'):
                raise PermissionDenied("Нет прав на отмену публикации")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """View для удаления продукта"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")
    context_object_name = "product"
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user

        if product.owner != user and not user.has_perm('catalog.delete_product'):
            raise PermissionDenied(
                "Вы не можете удалить этот продукт. ""Только владелец или модератор может удалять продукты.")
        return super().dispatch(request, *args, **kwargs)


class UnpublishProductView(LoginRequiredMixin, View):
    """Отмена публикации продукта (по заданию)"""

    def post(self, request, pk):
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied("У вас нет прав на отмену публикации")
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('catalog:product_list')
