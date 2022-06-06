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
