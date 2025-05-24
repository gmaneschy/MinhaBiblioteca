from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'tradutor', 'genero', 'npaginas', 'ano', 'preco', 'status', 'anotacoes']
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editora': 'Editora',
            'tradutor': 'Tradutor',
            'genero': 'Gênero',
            'npaginas': 'N° de Páginas',
            'ano': 'Ano de Publicação',
            'preco': 'Preço',
            'status': 'Status',
            'anotacoes': 'Anotações',
        }