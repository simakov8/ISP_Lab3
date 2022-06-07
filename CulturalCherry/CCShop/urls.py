from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/<int:gender>/<int:category>/', CatalogView.as_view(), name='catalog'),
    path('register/', SignUp.as_view(), name='register'),
    path('login/', SignIn.as_view(), name='login'),
]
