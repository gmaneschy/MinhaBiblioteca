from django import forms
from .models import Livro  # ajusta o nome conforme seu model

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'tradudor', 'genero', 'npaginas', 'ano', 'preco', 'status', 'anotacoes']  # coloque os campos corretos do seu model