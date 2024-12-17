from src.utils.sounds import play_enter, play_send, play_error, play_list, play_delete, play_created
from src.database.db_operations import listar_livros, inserir_livro, excluir_livro, listar_emprestimos
from src.utils.utils import gerar_isbn, checar_saida


def menu_livros():
    while True:
        print("\n--- Gerenciar Livros ---")
        print("1. Adicionar Livro ao Sistema")
        print("2. Procurar um Livro (por Nome ou ISBN)")
        print("3. Remover um Livro do Catálogo")
        print("4. Verificar Lista de Livros Emprestados")
        print("5. Voltar ao Menu Principal")

        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            print("Erro: Por favor, insira um número válido.")
            continue

        if opcao == 1:
            adicionar_livro()
        elif opcao == 2:
            procurar_livro()
        elif opcao == 3:
            remover_um_livro()
        elif opcao == 4:
            verificar_lista_emprestimos()
        elif opcao == 5:
            break
        else:
            print("Opção inválida. Tente novamente.")


def adicionar_livro():
    print("\n--- Adicionar Livro ---")
    play_enter()

    try:
        titulo = checar_saida(input("Título: ").strip())
        if not titulo:
            play_error()
            print("Ops! O campo 'Título' é obrigatório.")
            return

        autor = checar_saida(input("Autor: ").strip())
        if not autor:
            play_error()
            print("Ops! O campo 'Autor' é obrigatório.")
            return

        editora = checar_saida(input("Editora: ").strip())
        if not editora:
            play_error()
            print("Ops! O campo 'Editora' é obrigatório.")
            return

        genero = checar_saida(input("Gênero: ").strip())
        if not genero:
            play_error()
            print("Ops! O campo 'Gênero' é obrigatório.")
            return

        try:
            ano_publicacao = int(input("Ano de Publicação: ").strip())
            if ano_publicacao <= 0:
                play_error()
                print("Erro: O ano de publicação deve ser maior que zero.")
                return
        except ValueError:
            play_error()
            print("Erro: O ano de publicação deve ser um número inteiro.")
            return

        isbn = gerar_isbn()
        confirmacao = input(f"\nConfirma adicionar o livro '{titulo}' (ISBN: {isbn})? [S/N]: ").strip().lower()
        if confirmacao != "s":
            print("Operação cancelada. O livro não foi adicionado.")
            return

        inserir_livro(titulo, autor, editora, genero, ano_publicacao, isbn, disponivel=True)
        print(f"Livro '{titulo}' adicionado com sucesso! (ISBN: {isbn})")

    except SystemExit:
        return


def procurar_livro():
    print("\n--- Procurar Livro ---")
    try:
        criterio = checar_saida(input("Digite o Nome ou o ISBN do Livro: ").strip())
        if not criterio:
            print("Ops! O campo de busca é obrigatório.")
            return
    except SystemExit:
        return

    livros = listar_livros()
    resultados = [livro for livro in livros if criterio.lower() in livro["titulo"].lower() or criterio == livro["isbn"]]

    if not resultados:
        print("Nenhum livro encontrado.")
    else:
        print("\n--- Resultados da Busca ---")
        for livro in resultados:
            disponivel = "Sim" if livro["disponivel"] else "Não"
            print(f"Título: {livro['titulo']}, ISBN: {livro['isbn']}, Disponível: {disponivel}")


def remover_um_livro():
    print("\n--- Remover Livro ---")
    try:
        titulo = checar_saida(input("Digite o Título Completo do Livro: ").strip())
        if not titulo:
            print("Ops! O campo 'Título' é obrigatório.")
            return

        isbn = checar_saida(input("Digite o ISBN do Livro: ").strip())
        if not isbn:
            print("Ops! O campo 'ISBN' é obrigatório.")
            return

    except SystemExit:
        return

    livros = listar_livros()
    livro = next((livro for livro in livros if livro["titulo"].lower() == titulo.lower() and livro["isbn"] == isbn), None)

    if not livro:
        print("Erro: Livro não encontrado.")
        return

    confirmacao = input(f"\nTem certeza que deseja remover o livro '{titulo}' (ISBN: {isbn})? [S/N]: ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada. O livro não foi removido.")
        return

    excluir_livro(livro["id"])
    print("Livro removido com sucesso!")


def verificar_lista_emprestimos():
    print("\n--- Verificar Lista de Livros Emprestados ---")
    print("1. Verificar Lista Geral dos Empréstimos")
    print("2. Verificar Disponibilidade de um Livro pelo ID")

    try:
        opcao = int(input("\nEscolha uma opção: "))
    except ValueError:
        print("Erro: Por favor, insira um número válido.")
        return

    if opcao == 1:
        listar_todos_os_emprestimos()
    elif opcao == 2:
        verificar_disponibilidade_livro()
    else:
        print("Opção inválida.")


def listar_todos_os_emprestimos():
    print("\n--- Lista Geral de Empréstimos ---")
    emprestimos = listar_emprestimos()
    if not emprestimos:
        print("Nenhum empréstimo registrado.")
    else:
        for emprestimo in emprestimos:
            print(f"Livro: {emprestimo['livro_titulo']}, Cliente: {emprestimo['cliente_nome']}")


def verificar_disponibilidade_livro():
    print("\n--- Verificar Disponibilidade ---")
    try:
        livro_id = int(input("Digite o ID do Livro: ").strip())
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
        return

    livros = listar_livros()
    livro = next((livro for livro in livros if livro["id"] == livro_id), None)

    if not livro:
        print("Livro não encontrado.")
    else:
        status = "Disponível" if livro["disponivel"] else "Indisponível"
        print(f"O livro '{livro['titulo']}' está {status}.")
