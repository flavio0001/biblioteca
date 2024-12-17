import random

def gerar_Id_cliente():
    return random.randint(1000, 9999)

def gerar_isbn():
    return random.randint(1000000000000, 9999999999999)

def checar_saida(entrada):
    if entrada.strip().lower() == "exit":
        print("Voltando ao menu principal")
        raise SystemExit
    return entrada