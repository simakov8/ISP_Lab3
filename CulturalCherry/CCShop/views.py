from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *
from .utils import *


class HomeView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genders = Sex.objects.all()
        categories = Category.objects.all()
        context.update({
            'genders': genders,
            'categories': categories,
        })
        return context


def index(request):
    return HttpResponse('ccshop/views/index')


def second(request):
    return HttpResponse('ccshop/views/second')
