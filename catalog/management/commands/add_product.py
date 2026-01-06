from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add product to the database"

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Все существующие продукты и категории удалены")
        )

        call_command("loaddata", "category_fixture.json")
        self.stdout.write(self.style.SUCCESS("Фикстура категорий загружена"))

        call_command("loaddata", "product_fixture.json")
        self.stdout.write(self.style.SUCCESS("Фикстуры продуктов загружены"))

        # category, _ = Category.objects.get_or_create(
        #     name="Пылесос", description="для уборки дома"
        # )
        #
        # products = [
        #     {
        #         "name": "Philips",
        #         "description": "беспроводной с подсветкой и функцией мойки пола",
        #         "category": category,
        #         "price": 70000,
        #     },
        #     {
        #         "name": "Bosh",
        #         "description": "длинна провода 10 метров, сьемные насадки",
        #         "category": category,
        #         "price": 40000,
        #     }
        # ]
        #
        # for product_data in products:
        #     product, created = Product.objects.get_or_create(**product_data)
        #     if created:
        #         self.stdout.write(self.style.SUCCESS(f'Добавление продукта успешно:{product.name}'))
        #     else:
        #         self.stdout.write(self.style.WARNING(f'Продукт уже добавлен:{product.name}'))
