from src.models.livro import Livro
from src.models.cliente import Cliente

class Biblioteca:
    def __init__(self):
        self.lista_clientes_cadastrados = []  # Lista para armazenar clientes cadastrados
        self.catalogo_de_livros = []         # Lista para armazenar os livros do catálogo

    # Método para adicionar livros ao catálogo
    def adicionar_livros(self, livro):
        if not isinstance(livro, Livro):
            print("Erro: O objeto fornecido não é um livro válido.")
            return
        if not any(l.isbn == livro.isbn for l in self.catalogo_de_livros):
            self.catalogo_de_livros.append(livro)
            print(f"O livro '{livro.titulo}' foi adicionado ao catálogo.")
        else:
            print(f"O livro '{livro.titulo}' já está no catálogo.")

    # Método para remover um livro do catálogo
    def remover_livro(self, isbn):
        livro_removido = None
        for livro in self.catalogo_de_livros:
            if livro.isbn == isbn:
                livro_removido = livro
                break
        if livro_removido:
            self.catalogo_de_livros.remove(livro_removido)
            print(f"O livro '{livro_removido.titulo}' foi removido do catálogo.")
        else:
            print(f"Nenhum livro com ISBN '{isbn}' foi encontrado no catálogo.")

    # Método para listar todos os livros no catálogo
    def listar_catalogo(self):
        if not self.catalogo_de_livros:
            print("Nenhum livro no acervo.")
        else:
            print("=== Catálogo de Livros ===")
            for livro in self.catalogo_de_livros:
                print(livro.exibir_detalhes())
                print("-" * 30)

    # Método para listar todos os clientes cadastrados
    def listar_clientes_cadastrados(self):
        if not self.lista_clientes_cadastrados:
            print("Nenhum cliente cadastrado.")
        else:
            print("=== Clientes Cadastrados ===")
            for cliente in self.lista_clientes_cadastrados:
                print(f"Nome: {cliente.nome}, ID: {cliente.cliente_Id}")
