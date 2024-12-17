from src.menus.livro import menu_livros
from src.menus.usuarios import menu_usuarios

def menu_principal():
    while True:
        print("\n=== Seja bem vindo(a) ao gerenciador da livraria. ===")
        print("1. Gerenciador de livros")
        print("2. Gerenciador de usuários")
        print("3. Sair")

        try:
            opc = int(input("Digite uma opção"))
        except ValueError:
            print("Erro: Insira um número válido")
            continue

        try:
            if opc == 1:
                menu_livros()
            elif opc == 2:
                menu_usuarios()
            elif opc == 3:
                print("Enserrando o sistema! Até lógo!")
                break
            else:
                print("Opção inválida. Tente novamente")
        except SystemExit:
            continue

if __name__ == "__main__":
    menu_principal()