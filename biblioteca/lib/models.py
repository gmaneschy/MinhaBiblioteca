from django.db import models



# Create your models here.
class Livro(models.Model):
    titulo = models.CharField("Título", max_length=100)
    autor = models.CharField("Autor", max_length=100)
    editora = models.CharField("Editora", max_length=100)

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.editora}"

