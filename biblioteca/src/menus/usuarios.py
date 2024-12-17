from src.database.db_operations import listar_clientes, inserir_cliente, remover_cliente, listar_emprestimos
from src.utils.utils import gerar_Id_cliente, checar_saida


def menu_usuarios():
    while True:
        print("\n--- Gerenciar Usuários ---")
        print("1. Adicionar Novo Usuário")
        print("2. Verificar Lista de Usuários")
        print("3. Procurar por um Usuário e Ver os Livros em Seu Acervo")
        print("4. Remover um Usuário da Lista")
        print("5. Voltar ao Menu Principal")

        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            print("Erro: Por favor, insira um número válido.")
            continue

        if opcao == 1:
            adicionar_usuario()
        elif opcao == 2:
            listar_todos_os_usuarios()
        elif opcao == 3:
            verificar_acervo_usuario()
        elif opcao == 4:
            remover_um_usuario()
        elif opcao == 5:
            break
        else:
            print("Opção inválida. Tente novamente.")


def adicionar_usuario():
    print("\n--- Adicionar Novo Usuário ---")
    try:
        nome = checar_saida(input("Nome do Usuário: ").strip())
        if not nome:
            print("Ops! O campo 'Nome do Usuário' é obrigatório.")
            return

        id_cliente = gerar_Id_cliente()
        confirmacao = input(f"\nConfirma adicionar o usuário '{nome}' (ID: {id_cliente})? [S/N]: ").strip().lower()
        if confirmacao != "s":
            print("Operação cancelada. O usuário não foi adicionado.")
            return

        inserir_cliente(nome, id_cliente)
        print(f"Usuário '{nome}' adicionado com sucesso! (ID: {id_cliente})")

    except SystemExit:
        return


def listar_todos_os_usuarios():
    print("\n--- Lista de Usuários ---")
    clientes = listar_clientes()
    if not clientes:
        print("Nenhum usuário encontrado.")
    else:
        for cliente in clientes:
            print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, ID Cliente: {cliente['id_cliente']}")


def verificar_acervo_usuario():
    print("\n--- Verificar Acervo de um Usuário ---")
    try:
        nome = checar_saida(input("Digite o Nome Completo do Usuário: ").strip())
        if not nome:
            print("Ops! O campo 'Nome Completo do Usuário' é obrigatório.")
            return
    except SystemExit:
        return

    clientes = listar_clientes()
    cliente = next((c for c in clientes if c["nome"].lower() == nome.lower()), None)

    if not cliente:
        print(f"Erro: Usuário '{nome}' não encontrado.")
        return

    emprestimos = listar_emprestimos()
    acervo = [e for e in emprestimos if e["cliente_id"] == cliente["id"]]

    if not acervo:
        print(f"O usuário '{nome}' não possui livros emprestados.")
    else:
        print(f"\n--- Livros no Acervo do Usuário '{nome}' ---")
        for livro in acervo:
            print(f"Livro: {livro['livro_titulo']}, ISBN: {livro['livro_isbn']}")


def remover_um_usuario():
    print("\n--- Remover Usuário ---")
    try:
        nome = checar_saida(input("Digite o Nome Completo do Usuário: ").strip())
        if not nome:
            print("Ops! O campo 'Nome do Usuário' é obrigatório.")
            return

        id_cliente = checar_saida(input("Digite o ID do Usuário: ").strip())
        if not id_cliente:
            print("Ops! O campo 'ID do Usuário' é obrigatório.")
            return

    except SystemExit:
        return

    clientes = listar_clientes()
    cliente = next((c for c in clientes if c["nome"].lower() == nome.lower() and str(c["id_cliente"]) == id_cliente), None)

    if not cliente:
        print(f"Erro: Usuário '{nome}' com ID '{id_cliente}' não encontrado.")
        return

    confirmacao = input(f"\nTem certeza que deseja remover o usuário '{nome}' (ID: {id_cliente})? [S/N]: ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada. O usuário não foi removido.")
        return

    remover_cliente(cliente["id"])
    print(f"Usuário '{nome}' removido com sucesso!")
