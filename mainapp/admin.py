from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from PIL import Image


class FenceAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, ** kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red; front-size:14px;">Загружайте изображения с минимальным разрешением {}x{}</span>'.format(
                *Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должен превышать 3MB!")
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображение меньше минимального!')
        max_height, max_width = Product.MAX_RESOLUTION
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображение больше максимального!')
        return image


class FenceAdmin(admin.ModelAdmin):

    form = FenceAdminForm


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(TombstoneStrictForm)
admin.site.register(TombstoneUnusualForm)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Fence)

