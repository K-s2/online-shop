from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(self, *args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:
    objects = LatestProductManager()


class Category(models.Model):

    m_name = models.CharField(max_length=255, default=None)
    # slug = models.SlugField(unique=True)


class Product(models.Model):

    category = models.OneToOneField(Category, verbose_name="Категория", on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255, name="Наименование", default=None)
    # slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение", default=None)
    description = models.TextField(verbose_name="Описание", null="True", default=None)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена", default=None)


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products", default=None)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=None)
    object_id = models.PositiveIntegerField(default=None)
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена", default=None)

    def __str__(self):
        return "Продукт:{} (для корзины)".format(self.title)


class TombstoneStrictForm(Product):
    length = models.CharField(max_length=255, verbose_name="Длинна плиты строгой формы", default=None)
    width = models.CharField(max_length=255, verbose_name="Ширина плиты строгой формы", default=None)
    height = models.CharField(max_length=255, verbose_name="Высота строгой формы", default=None)


class TombstoneUnusualForm(Product):
    length = models.CharField(max_length=255, verbose_name="Длинна плиты необычной формы", default=None)
    width = models.CharField(max_length=255, verbose_name="Ширина плиты необычной формы", default=None)
    height = models.CharField(max_length=255, verbose_name="Высота плиты необычной формы", default=None)
    form = models.CharField(max_length=255, verbose_name="Форма плиты необычной формы", default=None)


class Fence(Product):
    length = models.CharField(max_length=255, verbose_name="Длинна забора", default=None)
    height = models.CharField(max_length=255, verbose_name="Высота забора", default=None)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name="Владелец", on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart", default=None)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена", default=None)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, default=None)
    phone = models.CharField(max_length=20, verbose_name="Номер Телефона", default=None)
    address = models.CharField(max_length=255, verbose_name="Адрес", default=None)

    def __str__(self):
        return "Покупатель:".format(self.first_name, self.user.last_name)




