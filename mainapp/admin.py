from django import forms
from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *


class TombstoneStrictFormCategoryChoiceField(forms.ModelChoiceField):

    pass


class TombstoneStrictFormAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug ='tombstonestricform'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(TombstoneStrictForm)
admin.site.register(TombstoneUnusualForm)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Fence)

