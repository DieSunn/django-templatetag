from django.contrib import admin
from django.urls import path
from .views import index, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('products/', index, name='products'), # Для теста
    path('products/phones/', index, name='phones'), # Для теста
    path('products/laptops/', index, name='laptops'), # Для теста
]