from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, RedirectView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm

class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('producto_list')

    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        return super().form_valid(form)

class LoginUsuarioView(LoginView):
    template_name = 'usuarios/login.html'

class LogoutUsuarioView(RedirectView):
    url = reverse_lazy('login_usuario')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
