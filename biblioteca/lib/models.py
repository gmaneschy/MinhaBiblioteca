from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

somente_letras_unicode = RegexValidator(
    regex=r'^[^\W\d_]+(?:\s[^\W\d_]+)*$',
)

# Create your models here.
class Livro(models.Model):
    class Status(models.TextChoices):
        LIDO = 'Lido', 'Lido'
        NAO_LIDO = 'Não lido', 'Não lido'

    titulo = models.CharField("Título", max_length=100)
    autor = models.CharField("Autor", max_length=100, validators=[somente_letras_unicode])
    editora = models.CharField("Editora", max_length=100)
    tradutor = models.CharField("Tradutor", max_length=100, blank=True, null=True, validators=[somente_letras_unicode])
    genero = models.CharField("Gênero", max_length=100, blank=True, null=True, validators=[somente_letras_unicode])
    npaginas = models.IntegerField("N° de Páginas", validators=[MaxValueValidator(9999), MinValueValidator(0)], default=0, blank=True, null=True)
    ano = models.IntegerField("Ano de Publicação", validators=[MaxValueValidator(9999), MinValueValidator(0)], default=0, blank=True, null=True)
    preco = models.DecimalField("Preço", max_digits=4, decimal_places=2, default=0.00, blank=True, null=True)
    status = models.CharField("Status", max_length=20, choices=Status.choices, default=Status.NAO_LIDO)
    anotacoes = models.TextField("Anotações", blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.editora} - {self.tradutor} - {self.genero} - {self.npaginas} - {self.ano} - {self.preco} - {self.status} - {self.anotacoes}"