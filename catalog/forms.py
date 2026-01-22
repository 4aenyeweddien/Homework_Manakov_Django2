from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm

from catalog.models import Product


class StyleFormMixin:
    """Миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    """Форма для создания и редактирования продуктов."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите наименование продукта"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание продукта"}
        )
        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Добавьте изображение продукта"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберите категорию продукта"}
        )
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите цену продукта"}
        )

    def clean_name(self):
        name = self.cleaned_data["name"].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f"Название содержит запрещенное слово: {word}")
        return self.cleaned_data["name"]

    def clean_description(self):
        description = self.cleaned_data["description"].lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f"Описание содержит запрещенное слово: {word}")
        return self.cleaned_data["description"]

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной")
        return price

class CatalogModeratorForm(StyleFormMixin, ModelForm):
