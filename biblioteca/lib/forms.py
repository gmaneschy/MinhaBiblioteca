from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Livro


User = get_user_model()

class LivroForm(forms.ModelForm):
    """
    Herda de forms.ModelForm e está associado ao modelo Livro.
        Campos incluídos: titulo, autor, editora, tradutor, genero, npaginas, ano, preco, status.
    Possui validações personalizadas:
        clean_tradutor(): Converte valores vazios ou "None" para None.
        clean_genero(): Similar à validação do tradutor.
        clean_preco(): Formata o preço, substituindo vírgula por ponto e convertendo para float.
    Inclui widgets personalizados com validações no lado do cliente (JavaScript) para formatar números, remover caracteres inválidos, etc.
    """
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
            'npaginas': forms.NumberInput(attrs={
                'min': 0,
                'max': 9999,
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '')",
                'onfocus': "if(this.defaultValue) this.value=''"
            }),
            'ano': forms.NumberInput(attrs={
                'min': 0,
                'max': 9999,
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '')",
                'onfocus': "if(this.defaultValue) this.value=''"
            }),
            'preco': forms.TextInput(attrs={
                'inputmode': 'decimal',
                'oninput': r"this.value = this.value.replace(/[^0-9.,]/g, '')",
                'onfocus': "if(this.defaultValue) this.value=''"
            }),
            'tradutor': forms.TextInput(attrs={
                'pattern': r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
                'title': 'Apenas letras (sem números ou símbolos)',
                'oninput': r"this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '')"
            }),
            'genero': forms.TextInput(attrs={
                'pattern': r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
                'title': 'Apenas letras (sem números ou símbolos)',
                'oninput': r"this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '')"
            }),
            'autor': forms.TextInput(attrs={
                'pattern': r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
                'title': 'Apenas letras (sem números ou símbolos)',
                'oninput': r"this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, '')"
            }),
            'status': forms.Select()
        }
        def clean_tradutor(self):
            valor = self.cleaned_data.get('tradutor')
            return None if valor in ["", "None"] else valor

        def clean_genero(self):
            valor = self.cleaned_data.get('genero')
            return None if valor in ["", "None"] else valor

        def clean_preco(self):
            preco = self.cleaned_data.get('preco')
            if isinstance(preco, str):
                preco = preco.replace(',', '.')
            try:
                return float(preco)
            except (ValueError, TypeError):
                raise forms.ValidationError("Preço inválido. Use números.")

class CustomUserCreationForm(forms.Form):
    """
    Formulário personalizado para criação de usuários.
    Campos: username, email, password1, password2.
    Validações:
        clean_username(): Verifica se o nome de usuário já existe.
        clean_email(): Verifica se o e-mail já está em uso.
        clean_password2(): Confirma se as senhas são iguais.
        Metodo save(): Cria e salva um novo usuário com os dados fornecidos, garantindo que não seja staff nem superusuário.
    """
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
    """
    Estende o formulário de autenticação padrão do Django.
    Personaliza o campo username para aceitar tanto nome de usuário quanto e-mail.
    Sobrescreve o metodo clean() para permitir login com e-mail, convertendo-o para o nome de usuário correspondente antes da autenticação.
    """
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
