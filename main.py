class Livro:
    def __init__(self, titulo):
        self.titulo = titulo
        print(titulo)

arquivo = []
def registrar_livro():
    titulo = input("Digite o título do livro: ")
    arquivo.append(titulo)
    return Livro(titulo)

registrar_livro()

print(*arquivo)