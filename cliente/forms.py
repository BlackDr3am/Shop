from django import forms
from productos.models import Usuario  # O desde donde esté tu modelo personalizado

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
