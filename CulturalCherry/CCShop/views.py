from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('ccshop/views/index')


def second(request):
    return HttpResponse('ccshop/views/second')
