from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import OperationalError
from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm

class ProductoListView(ListView):
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        try:
            return Producto.objects.all()
        except OperationalError:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['categorias'] = Producto.objects.values_list('categoria', flat=True).distinct()
        except OperationalError:
            context['categorias'] = []
        return context

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except OperationalError:
            return render(self.request, 'error_base_datos.html')

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except OperationalError:
            return render(self.request, 'error_base_datos.html')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except OperationalError:
            return render(request, 'error_base_datos.html')
