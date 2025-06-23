from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Producto, ImagenProducto, Categoria

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2']

class ProductoForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'categorias']

class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['producto', 'imagen']
