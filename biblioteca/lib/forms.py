from django import forms
from .models import Livro  # ajusta o nome conforme seu model

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora']  # coloque os campos corretos do seu model
        # 'tradutor', 'genero', 'npaginas', 'ano', 'preco', 'status', 'anotacoes'