from src.database.db_config import conectar_mysql

def inserir_livro(titulo, autor, editora, genero, ano_publicacao, isbn, disponivel=True):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM livros WHERE isbn = %s", (isbn,))
        if cursor.fetchone():
            print(f"Erro: Já existe um livro com o ISBN '{isbn}' no sistema.")
            return
        query = '''
            INSERT INTO livros (titulo, autor, editora, genero, ano_publicacao, isbn, disponivel)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        valores = (titulo, autor, editora, genero, ano_publicacao, isbn, disponivel)
        cursor.execute(query, valores)
        conexao.commit()
        print(f"Livro '{titulo}' inserido com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir livro: {e}")
    finally:
        conexao.close()

def inserir_cliente(nome, id_cliente):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM clientes WHERE id_cliente = %s", (id_cliente,))
        if cursor.fetchone():
            print(f"Erro: Já existe um cliente com o ID '{id_cliente}' no sistema.")
            return
        query = '''
            INSERT INTO clientes (nome, id_cliente)
            VALUES (%s, %s)
        '''
        valores = (nome, id_cliente)
        cursor.execute(query, valores)
        conexao.commit()
        print(f"Cliente '{nome}' inserido com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir cliente: {e}")
    finally:
        conexao.close()

def registrar_emprestimo(cliente_id, livro_id, data_emprestimo):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
        if not cursor.fetchone():
            print("Erro: Cliente não encontrado.")
            return
        cursor.execute("SELECT COUNT(*) FROM emprestimos WHERE cliente_id = %s AND data_devolucao IS NULL", (cliente_id,))
        if cursor.fetchone()[0] >= 3:
            print("Erro: O cliente já possui o número máximo de livros emprestados.")
            return
        cursor.execute("SELECT disponivel FROM livros WHERE id = %s", (livro_id,))
        resultado = cursor.fetchone()
        if not resultado or resultado[0] == 0:
            print("Erro: O livro não está disponível para empréstimo.")
            return
        query = '''
            INSERT INTO emprestimos (cliente_id, livro_id, data_emprestimo)
            VALUES (%s, %s, %s)
        '''
        valores = (cliente_id, livro_id, data_emprestimo)
        cursor.execute(query, valores)
        cursor.execute("UPDATE livros SET disponivel = 0 WHERE id = %s", (livro_id,))
        conexao.commit()
        print("Empréstimo registrado com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar empréstimo: {e}")
    finally:
        conexao.close()

def listar_livros(apenas_disponiveis=False):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT * FROM livros"
        if apenas_disponiveis:
            query += " WHERE disponivel = 1"
        cursor.execute(query)
        livros = cursor.fetchall()
        return livros
    except Exception as e:
        print(f"Erro ao listar livros: {e}")
        return []
    finally:
        conexao.close()

def listar_clientes():
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor(dictionary=True)
        query = "SELECT * FROM clientes"
        cursor.execute(query)
        clientes = cursor.fetchall()
        return clientes
    except Exception as e:
        print(f"Erro ao listar clientes: {e}")
        return []
    finally:
        conexao.close()

def registrar_devolucao(emprestimo_id, data_devolucao):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        query = '''
            UPDATE emprestimos
            SET data_devolucao = %s
            WHERE id = %s
        '''
        cursor.execute(query, (data_devolucao, emprestimo_id))
        cursor.execute('''
            UPDATE livros
            SET disponivel = 1
            WHERE id = (
                SELECT livro_id FROM emprestimos WHERE id = %s
            )
        ''', (emprestimo_id,))
        conexao.commit()
        print("Devolução registrada com sucesso!")
    except Exception as e:
        print(f"Erro ao registrar devolução: {e}")
    finally:
        conexao.close()

def excluir_livro(livro_id):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM emprestimos WHERE livro_id = %s AND data_devolucao IS NULL", (livro_id,))
        if cursor.fetchone():
            print("Erro: Não é possível excluir um livro que está emprestado.")
            return
        query = "DELETE FROM livros WHERE id = %s"
        cursor.execute(query, (livro_id,))
        conexao.commit()
        print("Livro excluído com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir livro: {e}")
    finally:
        conexao.close()

def remover_cliente(cliente_id):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM emprestimos WHERE cliente_id = %s AND data_devolucao IS NULL", (cliente_id,))
        if cursor.fetchone():
            print("Erro: Não é possível remover um cliente com empréstimos ativos.")
            return
        query = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(query, (cliente_id,))
        conexao.commit()
        print("Cliente removido com sucesso!")
    except Exception as e:
        print(f"Erro ao remover cliente: {e}")
    finally:
        conexao.close()

def listar_emprestimos(apenas_ativos=False):
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor(dictionary=True)
        query = '''
            SELECT e.id, e.cliente_id, e.livro_id, e.data_emprestimo, e.data_devolucao,
                   c.nome AS cliente_nome, l.titulo AS livro_titulo
            FROM emprestimos e
            INNER JOIN clientes c ON e.cliente_id = c.id
            INNER JOIN livros l ON e.livro_id = l.id
        '''
        if apenas_ativos:
            query += " WHERE e.data_devolucao IS NULL"
        cursor.execute(query)
        emprestimos = cursor.fetchall()
        return emprestimos
    except Exception as e:
        print(f"Erro ao listar empréstimos: {e}")
        return []
    finally:
        conexao.close()
