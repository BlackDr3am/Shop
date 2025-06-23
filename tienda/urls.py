from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),  # o tienda.urls si ahí están tus vistas principales
    path('usuarios/', include('cliente.urls')),  # nuevo
]
