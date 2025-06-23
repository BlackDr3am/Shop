from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Producto, ImagenProducto, Carrito, Envio, Usuario, Categoria
from .forms import RegistroUsuarioForm, ProductoForm, ImagenProductoForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

class RegistroUsuarioView(CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('producto_list')

    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        return redirect(self.success_url)  # 👈 Aquí está el redirect correcto

class LoginUsuarioView(LoginView):
    template_name = 'usuarios/login.html'

class LogoutUsuarioView(LogoutView):
    next_page = reverse_lazy('productos/producto_list.html')

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/producto_list.html'

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

class ImagenProductoCreateView(LoginRequiredMixin, CreateView):
    model = ImagenProducto
    form_class = ImagenProductoForm
    template_name = 'productos/agregar_imagen.html'
    success_url = reverse_lazy('producto_list')

class FinalizarCompraView(LoginRequiredMixin, CreateView):
    model = Envio
    template_name = 'productos/finalizar_compra.html'
    success_url = reverse_lazy('confirmacion_envio')

    def form_valid(self, form):
        usuario = self.request.user
        carrito = Carrito.objects.get(usuario=usuario)

        envio = form.save(commit=False)
        envio.usuario = usuario
        envio.direccion = usuario.direccion
        envio.save()
        envio.productos.set(carrito.productos.all())

        carrito.productos.clear()
        return super().form_valid(form)

class ProductoFiltradoListView(ListView):
    model = Producto
    template_name = 'producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        q = self.request.GET.get('q')
        cat = self.request.GET.get('categoria')
        precio = self.request.GET.get('precio_max')
        queryset = super().get_queryset()
        if q: queryset = queryset.filter(nombre__icontains=q)
        if cat: queryset = queryset.filter(categorias__id=cat)
        if precio: queryset = queryset.filter(precio__lte=precio)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context
