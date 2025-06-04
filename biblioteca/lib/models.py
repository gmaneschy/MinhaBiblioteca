from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model
somente_letras_unicode = RegexValidator(
    regex=r'^[^\W\d_]+(?:\s[^\W\d_]+)*$',
)
User = get_user_model()
# Create your models here.
class Livro(models.Model):
    class Status(models.TextChoices):
        LIDO = 'Lido', 'Lido'
        NAO_LIDO = 'Não lido', 'Não lido'
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros')
    titulo = models.CharField("Título", max_length=100)
    autor = models.CharField("Autor", max_length=100, validators=[somente_letras_unicode])
    editora = models.CharField("Editora", max_length=100)
    tradutor = models.CharField("Tradutor", max_length=100, blank=True, null=True, validators=[somente_letras_unicode])
    genero = models.CharField("Gênero", max_length=100, blank=True, null=True, validators=[somente_letras_unicode])
    npaginas = models.IntegerField("N° de Páginas", validators=[MaxValueValidator(9999), MinValueValidator(0)], default=0, blank=True, null=True)
    ano = models.IntegerField("Ano de Publicação", validators=[MaxValueValidator(9999), MinValueValidator(0)], default=0, blank=True, null=True)
    preco = models.DecimalField("Preço", max_digits=6, decimal_places=2, default=0.00, blank=True, null=True)
    status = models.CharField("Status", max_length=20, choices=Status.choices, default=Status.NAO_LIDO)
    anotacoes = models.TextField("Anotações", blank=True, null=True)
    def save(self, *args, **kwargs):
        campos_opcionais = ['tradutor', 'genero', 'anotacoes']
        for campo in campos_opcionais:
            valor = getattr(self, campo)
            if valor in ["", "None"]:
                setattr(self, campo, None)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.editora} - {self.tradutor} - {self.genero} - {self.npaginas} - {self.ano} - {self.preco} - {self.status} - {self.anotacoes}"


class Biblioteca(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='biblioteca')
    nome = models.CharField("Nome da Biblioteca", max_length=100, default="Minha biblioteca")
    descricao = models.TextField("Descrição da Biblioteca", max_length=1000, blank=True, default="")
    def save(self, *args, **kwargs):
        if not self.nome.strip():
            self.nome = "Minha biblioteca"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def criar_biblioteca(sender, instance, created, **kwargs):
    if created:
        Biblioteca.objects.create(usuario=instance)