from src.utils.utils import gerar_Id_cliente

class Cliente:
    def __init__(self, nome, livros_emprestados=None):
        self.__nome = nome
        self.__cliente_Id = gerar_Id_cliente()  # ID gerado automaticamente
        self.__livros_emprestados = livros_emprestados if livros_emprestados else []

    # Getters
    @property
    def nome(self):
        return self.__nome

    @property
    def cliente_Id(self):
        return self.__cliente_Id

    @property
    def livros_emprestados(self):
        return self.__livros_emprestados

    # Setters
    @nome.setter
    def nome(self, nome):
        if not nome.strip():
            raise ValueError("O nome do cliente não pode ser vazio.")
        self.__nome = nome

    @livros_emprestados.setter
    def livros_emprestados(self, livros):
        if not isinstance(livros, list):
            raise ValueError("Os livros emprestados devem ser uma lista.")
        for livro in livros:
            if not hasattr(livro, "titulo") or not hasattr(livro, "autor") or not hasattr(livro, "disponibilidade"):
                raise ValueError(
                    "Todos os itens da lista de livros emprestados devem ser instâncias válidas de um objeto Livro."
                )
        self.__livros_emprestados = livros

    # Métodos para manipular livros emprestados
    def emprestar_livro(self, livro):
        if not livro.disponibilidade:
            print(f"Erro: O livro '{livro.titulo}' já está emprestado.")
            return
        livro.emprestar()
        self.__livros_emprestados.append(livro)
        print(f"O livro '{livro.titulo}' foi emprestado com sucesso!")

    def devolver_livro(self, livro):
        if livro not in self.__livros_emprestados:
            print(f"Erro: O cliente não possui o livro '{livro.titulo}' emprestado.")
            return
        livro.devolver()
        self.__livros_emprestados.remove(livro)
        print(f"O livro '{livro.titulo}' foi devolvido com sucesso!")

    def listar_livros_emprestados(self):
        if not self.__livros_emprestados:
            print("O cliente não possui livros emprestados.")
        else:
            print("Livros emprestados atualmente pelo cliente:")
            for livro in self.__livros_emprestados:
                print(f"{livro.titulo} de {livro.autor}")
