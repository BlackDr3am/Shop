from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import OperationalError
from .forms import RegistroForm
from productos.models import Usuario  # Si estás usando un modelo personalizado

class LoginUsuarioView(LoginView):
    template_name = 'usuarios/login.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except OperationalError:
            return render(request, 'error_base_datos.html')

class LogoutUsuarioView(LogoutView):
    next_page = reverse_lazy('login_usuario')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except OperationalError:
            return render(request, 'error_base_datos.html')

class RegistroUsuarioView(CreateView):
    model = Usuario
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login_usuario')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except OperationalError:
            return render(self.request, 'error_base_datos.html')

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})
