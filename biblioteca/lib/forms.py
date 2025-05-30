from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Livro


User = get_user_model()

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'tradutor', 'genero', 'npaginas', 'ano', 'preco', 'status']
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
        }
        widgets = {
            'npaginas': forms.NumberInput(attrs={'min': 0, 'max': 9999, 'oninput': "this.value = this.value.replace(/[^0-9]/g, '')"}),
            'ano': forms.NumberInput(attrs={'min': 0, 'max': 9999, 'oninput': "this.value = this.value.replace(/[^0-9]/g, '')"}),
            'preco': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'oninput': "this.value = this.value.replace(/[^0-9.,]/g, '')"}),
            'tradutor': forms.TextInput(attrs={
                'pattern': r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
                'title': 'Apenas letras (sem números ou símbolos)',
                'oninput': "this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '')"
            }),
            'genero': forms.TextInput(attrs={
                'pattern': r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
                'title': 'Apenas letras (sem números ou símbolos)',
                'oninput': "this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '')"
            }),
            'autor': forms.TextInput(attrs={
                'pattern': r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
                'title': 'Apenas letras (sem números ou símbolos)',
                'oninput': "this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '')"
            }),
            'status': forms.Select()
        }


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Nome do usuário', min_length=4, max_length=150)
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', min_length=8, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Nome do usuário já existe")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Já existe uma conta com este e-mail")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não são iguais")

        return password2

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            is_staff=False,  # Garante que não é staff/admin
            is_superuser=False  # Garante que não é superuser
        )
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuário ou E-mail')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Verifica se é um e-mail e tenta buscar o username
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                pass  # Continua com o valor original

        return super().clean()
