from django import forms
from .models import Livro  # ajusta o nome conforme seu model

class LivroFormSimples(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora']
        labels = {
            'titulo': 'Título*',
            'autor': 'Autor*',
            'editora': 'Editora*'
        }

class LivroFormAvancado(forms.ModelForm):
    mostrar_tradutor = forms.BooleanField(
        label='Mostrar tradutor na tabela',
        required=False,
        initial=True
    )
    mostrar_genero = forms.BooleanField(
        label='Mostrar gênero na tabela',
        required=False,
        initial=True
    )
    mostrar_npaginas = forms.BooleanField(
        label='Mostrar número de páginas na tabela',
        required=False,
        initial=True
    )
    mostrar_ano = forms.BooleanField(
        label='Mostrar ano de publicação na tabela',
        required=False,
        initial=True
    )
    mostrar_preco = forms.BooleanField(
        label='Mostrar preço na tabela',
        required=False,
        initial=True
    )
    mostrar_status = forms.BooleanField(
        label='Mostrar status na tabela',
        required=False,
        initial=True
    )

    class Meta:
        model = Livro
        fields = '__all__'
        widgets = {
            'anotacoes': forms.Textarea(attrs={'rows': 3}),
            'status': forms.RadioSelect
        }