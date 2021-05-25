from django.shortcuts import render
from django.views.generic import DetailView
from .models import Fence, TombstoneUnusualForm, TombstoneStrictForm, Category


def test_view(request):
    print(Category.objects.get_categories_for_left_sidebar())
    return render(request, 'base.html')


class ProductDetailVeiw(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'fence': Fence,
        'tombstonestrictform': TombstoneStrictForm,
        'tombstoneunusualform': TombstoneUnusualForm
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        print(self.model)
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
