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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['titulo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Título'})
            self.fields['autor'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Autor'})
            self.fields['editora'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Editora'})
            self.fields['tradutor'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tradutor'})
            self.fields['genero'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Gênero'})
            self.fields['npaginas'].widget.attrs.update({'class': 'form-control', 'placeholder': 'N° de Páginas'})
            self.fields['ano'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ano de Publicação'})
            self.fields['preco'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Preço'})
            self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Status'})
            self.fields['anotacoes'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Anotações'})