import textwrap
   
def menu():
    menu = """\n
    ========== MENU ==========
    
    [0]\tNovo usuário
    [1]\tNova conta
    [3]\tDepositar
    [4]\tSacar
    [5]\tExtrato
    [6]\tListar contas
   
    [s]\tSair

    >"""
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n *** Depósito realizado com sucesso! *** ")
    else:
        print("\n [COD 020] Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("[cod 017] Operação falhou: Você não tem saldo suficiente.")
        print("".center(40, "="))

    elif excedeu_limite:
        print("[cod 016] Operação falhou: Saque excede o limite diário.")
        print("".center(40, "="))

    elif excedeu_saques:
        print("[cod 015] Operação falhou: Número máximo de saques diários excedido.")
        print("".center(40, "="))

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(" *** Operação com Sucesso! *** ".center(40, " "))
        print("".center(40, "="))

    else:
        print("[cod 010]Operação falhou: O valor informado é inválido.")
        print("".center(40, "="))
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
            print(" ESTRATO ".center(40, "="))
            print("[cod 004] Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("".center(40, "="))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuarios:
        print("\n[cod 040] Já existe usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print(" *** Usuário criado com sucesso! ***")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(AGENCIA, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario}

    print("\n[COD 050] Usuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    
    LIMITES_SAQUES = 3
    AGENCIA = "001"   
    
    saldo = 0
    limite = 1000
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    
    while True:
        opção = menu()
            
        if opção == "0":
            criar_usuario(usuarios)

        elif opção == "1":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opção == "3":
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opção == "4":
            valor = float(input("Informe o valor desejado saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITES_SAQUES,
            )

        elif opção == "5":
            exibir_extrato(saldo, extrato=extrato)

        elif opção == "6":
            listar_contas(contas)
            
        elif opção == "s":
                break    
            
        else:
            print("[cod 085] Opção inválida: Por favor selecione novamente a operação desejada.")
            print("".center(38, "="))

main()  