from django import forms
from .models import Livro, Login
from django.core.exceptions import ValidationError

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'tradutor', 'genero', 'npaginas', 'ano', 'preco']
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'editora': 'Editora',
            'tradutor': 'Tradutor',
            'genero': 'Gênero',
            'npaginas': 'N° de Páginas',
            'ano': 'Ano de Publicação',
            'preco': 'Preço',
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email', 'senha']
        labels = {
            'email': 'E-mail',
            'senha': 'Senha',
        }
        widgets = {
            'senha': forms.PasswordInput(),
        }

class RegistroForm(forms.ModelForm):
    confirmar_senha = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = ['email', 'senha']
        labels = {
            'email': 'E-mail',
            'senha': 'Senha',
        }
        widgets = {
            'senha': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmar = cleaned_data.get("confirmar_senha")

        if senha and confirmar and senha != confirmar:
            raise ValidationError("As senhas não coincidem.")