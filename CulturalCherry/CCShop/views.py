from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *
from .forms import SignUpForm, SignInForm
from .utils import *
from django.contrib import messages


class HomeView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/index.html'
    extra_context = {'title': 'CulturalCherry'}


class CatalogView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/catalog.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Каталог',
            'gender': Sex.objects.get(pk=self.kwargs['gender']),
            'category': Category.objects.get(pk=self.kwargs['category']),
        })
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['category'], sex=self.kwargs['gender'])


class SignUp(HeaderView, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'CCShop/authentication.html'

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context.update({
            'title': 'Регистрация',
            'form_button': 'Регистрация',
        })
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно зарегистрировались')
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка регистрации')
        return super(SignUp, self).form_invalid(form)


class SignIn(HeaderView, LoginView):
    authentication_form = SignInForm
    template_name = 'CCShop/authentication.html'
    redirect_field_name = '/'

    def get_context_data(self, **kwargs):
        context = super(SignIn, self).get_context_data(**kwargs)
        context.update({
            'title': 'Вход',
            'form_button': 'Вход',
        })
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин и/или пароль')
        return super(SignIn, self).form_invalid(form)
