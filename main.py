from fasthtml.common import fast_app, serve, Titled, RedirectResponse
from componentes import reg_livro
app, routes = fast_app()

class Livro:
    def __init__(self, titulo, autor, editora):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        print(titulo)

arquivo = []

@routes("/home")
def homepage():
    reg = registrar_livro()
    return reg

def registrar_livro():
    titulo = input("Livro: ")
    autor = input("Autor: ")
    editora = input("Editora: ")

    # arquivo.append(titulo)
    return Livro(titulo, autor, editora)


print(*arquivo)
