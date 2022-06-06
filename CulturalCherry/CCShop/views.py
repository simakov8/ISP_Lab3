from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *
from .utils import *


class HomeView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/index.html'


class CatalogView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/catalog.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'gender': Sex.objects.get(pk=self.kwargs['gender']),
            'category': Category.objects.get(pk=self.kwargs['category']),
        })
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['category'], sex=self.kwargs['gender'])
