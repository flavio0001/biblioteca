from src.utils.utils import gerar_isbn

class Livro:
    def __init__(self, titulo, autor, editora, genero, ano, disponibilidade=True):
        self.__titulo = titulo
        self.__autor = autor
        self.editora = editora
        self.genero = genero
        self.__ano = ano
        self.__isbn = gerar_isbn()  # ISBN gerado automaticamente
        self.__disponibilidade = disponibilidade

    # Propriedades (Getters)
    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def ano(self):
        return self.__ano

    @property
    def isbn(self):  # Getter para acessar o ISBN gerado
        return self.__isbn

    @property
    def disponibilidade(self):
        return self.__disponibilidade

    # Propriedades (Setters)
    @titulo.setter
    def titulo(self, titulo):
        if not titulo.strip():
            raise ValueError("O título do livro não pode ser vazio.")
        self.__titulo = titulo

    @autor.setter
    def autor(self, autor):
        if not autor.strip():
            raise ValueError("O nome do autor não pode ser vazio.")
        self.__autor = autor

    @ano.setter
    def ano(self, ano):
        if not str(ano).isdigit():
            raise ValueError("O ano deve ser um número.")
        if int(ano) < 0:
            raise ValueError("O ano deve ser maior ou igual a 0.")
        self.__ano = ano

    @disponibilidade.setter
    def disponibilidade(self, disponibilidade):
        if not isinstance(disponibilidade, bool):
            raise ValueError("A disponibilidade deve ser um valor booleano (True ou False).")
        self.__disponibilidade = disponibilidade

    # Métodos
    def exibir_detalhes(self):
        return (
            f"Título: {self.titulo}\n"
            f"Autor: {self.autor}\n"
            f"Editora: {self.editora}\n"
            f"Gênero: {self.genero}\n"
            f"Ano de publicação: {self.ano}\n"
            f"ISBN: {self.isbn}\n"
            f"Disponível: {'Sim' if self.disponibilidade else 'Não'}"
        )

    def emprestar(self):
        if self.disponibilidade:
            self.disponibilidade = False
            print(f"O livro '{self.titulo}' foi emprestado.")
        else:
            print(f"O livro '{self.titulo}' já está emprestado.")

    def devolver(self):
        if not self.disponibilidade:
            self.disponibilidade = True
            print(f"O livro '{self.titulo}' foi devolvido.")
        else:
            print(f"O livro '{self.titulo}' já está disponível.")
