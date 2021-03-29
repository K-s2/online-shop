from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
User = get_user_model()


class LatestProductsManager:

    def get_products_for_main_page(self, *args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        return products


class LatestProducts:

    object = LatestProductsManager()


class Category(models.Model):

    m_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.id)


class Product(models.Model):

    class Meta:
         abstract = True

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", null="True")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return "Продукт:{} (для корзины)".format(self.product.title)


class TombstoneStrictForm(Product):

    length = models.CharField(max_length=255, verbose_name="Длинна плиты строгой формы")
    width = models.CharField(max_length=255, verbose_name="Ширина плиты строгой формы")
    height = models.CharField(max_length=255, verbose_name="Высота строгой формы")

    def __str__(self):
        return"{} : {}".format(self.category.name, self.title)


class TombstoneUnusualForm(Product):

    length = models.CharField(max_length=255, verbose_name="Длинна плиты необычной формы")
    width = models.CharField(max_length=255, verbose_name="Ширина плиты необычной формы")
    height = models.CharField(max_length=255, verbose_name="Высота плиты необычной формы")
    form = models.CharField(max_length=255, verbose_name="Форма плиты необычной формы")

    def __str__(self):
        return"{} : {}".format(self.category.name, self.title)


class Fence(Product):
    length = models.CharField(max_length=255, verbose_name="Длинна забора")
    height = models.CharField(max_length=255, verbose_name="Высота забора")

    def __str__(self):
        return"{} : {}".format(self.category.name, self.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая цена")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер Телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return "Покупатель:".format(self.first_name, self.user.last_name )




