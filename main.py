class Livro:
    def __init__(self, titulo, autor, editora):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        print(titulo)

arquivo = []

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