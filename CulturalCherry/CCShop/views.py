import logging

from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from .models import *
from .forms import SignUpForm, SignInForm, AddToCartForm, MakeOrderForm
from .utils import *
from django.contrib import messages


logger = logging.getLogger('logger')


class HomeView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/index.html'
    extra_context = {'title': 'CulturalCherry'}


class CatalogView(HeaderView, ListView):
    model = Product
    template_name = 'CCShop/catalog.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        logger.info('CatalogView.get_context_data')

        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Каталог',
            'gender': Sex.objects.get(pk=self.kwargs['gender']),
            'category': Category.objects.get(pk=self.kwargs['category']),
        })
        return context

    def get_queryset(self):
        logger.info('CatalogView.get_queryset')

        return Product.objects.filter(category=self.kwargs['category'], sex=self.kwargs['gender'])


class SignUp(HeaderView, CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'CCShop/authentication.html'

    def get_context_data(self, **kwargs):
        logger.info('SignUp.get_context_data')

        context = super(SignUp, self).get_context_data(**kwargs)
        context.update({
            'title': 'Регистрация',
            'form_button': 'Регистрация',
        })
        return context

    def form_valid(self, form):
        logger.info('SignUp.form_valid')

        messages.success(self.request, 'Вы успешно зарегистрировались')
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.info('SignUp.form_valid')

        messages.error(self.request, 'Ошибка регистрации')
        return super(SignUp, self).form_invalid(form)


class SignIn(HeaderView, LoginView):
    authentication_form = SignInForm
    template_name = 'CCShop/authentication.html'
    redirect_field_name = '/'

    def get_context_data(self, **kwargs):
        logger.info('SignIn.get_context_data')

        context = super(SignIn, self).get_context_data(**kwargs)
        context.update({
            'title': 'Вход',
            'form_button': 'Вход',
        })
        return context

    def form_invalid(self, form):
        logger.info('SignIn.form_invalid')

        messages.error(self.request, 'Ошибка входа')
        return super(SignIn, self).form_invalid(form)


class ProductView(HeaderView, FormView):
    form_class = AddToCartForm
    template_name = 'CCShop/product.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        logger.info('ProductView.get_context_data')

        context = super(ProductView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Продукт',
            'product': Product.objects.get(pk=self.kwargs['product_id'])
        })
        return context

    def form_valid(self, form):
        logger.info('ProductView.form_valid')

        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Для добавления в корзину войдите в аккаунт')
            return redirect('login')

        if Cart.objects.filter(product=self.kwargs['product_id']).exists():
            Cart.objects.filter(product=self.kwargs['product_id']).update(count=F('count') + form.cleaned_data['count'])
        else:
            cart = Cart()
            user = User.objects.get(pk=self.request.user.pk)
            cart.user = user
            cart.product = Product.objects.get(pk=self.kwargs['product_id'])
            cart.count = form.cleaned_data['count']
            cart.save()
        return super().form_valid(form)


class CartView(HeaderView, FormView):
    form_class = MakeOrderForm
    template_name = 'CCShop/cart.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        logger.info('CartView.get_context_data')

        context = super(CartView, self).get_context_data(**kwargs)
        preorders = Cart.objects.filter(user=self.request.user.pk)
        products_pk = preorders.values_list('product', flat=True)
        products = []
        for i in products_pk:
            products.append(Product.objects.get(pk=i))

        orders = zip(range(1, preorders.count() + 1), products, preorders)
        context.update({
            'preorders': orders,
        })
        return context

    def form_valid(self, form):
        logger.info('CartView.form_valid')

        preorders = Cart.objects.filter(user=self.request.user.pk)
        for preorder in preorders:
            order = Order()
            user = User.objects.get(pk=self.request.user.pk)
            order.user = user
            order.count = preorder.count
            order.product = preorder.product
            order.save()
        preorders.delete()
        return super().form_valid(form)


class SignOutView(HeaderView, LogoutView):
    next_page = '/'
