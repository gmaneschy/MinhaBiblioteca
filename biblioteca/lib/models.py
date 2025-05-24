from django.db import models



# Create your models here.
class Livro(models.Model):
    class Status(models.TextChoices):
        LIDO = 'Lido', 'Lido'
        NAO_LIDO = 'Não lido', 'Não lido'

    titulo = models.CharField("Título", max_length=100)
    autor = models.CharField("Autor", max_length=100)
    editora = models.CharField("Editora", max_length=100)
    tradutor = models.CharField("Tradutor", max_length=100, blank=True, null=True)
    genero = models.CharField("Gênero", max_length=100, blank=True, null=True)
    npaginas = models.IntegerField("N° de Páginas", default=0, blank=True, null=True)
    ano = models.IntegerField("Ano de Publicação", default=0, blank=True, null=True)
    preco = models.DecimalField("Preço", max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.NAO_LIDO
    )
    anotacoes = models.TextField("Anotações", blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.editora} - {self.tradutor} - {self.genero} - {self.npaginas} - {self.ano} - {self.preco} - {self.status} - {self.anotacoes}"

