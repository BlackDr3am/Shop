from django.urls import path
from .views import ProductoListView  # importa tus vistas aquí

urlpatterns = [
    path('', ProductoListView.as_view(), name='producto_list'),
]
