def menu():
    menu = """

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        [nu] criar Novo usuário
        [nc] Criar nova conta
        [l] Listar contas

    ==> """
    opcao = input(menu)
    return opcao



def saque(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saques):

    se_excedeu_saldo = True if valor_saque > saldo else False
    se_excedeu_saques = True if numero_saques >= limite_saques else False
    se_excedeu_limite = True if valor_saque > limite else False
    if valor_saque> 0:
        if se_excedeu_limite:
            print("Limite de transferencia excedido, não foi possível realizar a operação ")
            return(saldo, extrato)
        else:
            if se_excedeu_saldo & se_excedeu_saques:
                print("Saldo e saques insuficientes")
            elif ~se_excedeu_saldo & se_excedeu_saques:
                print("Saques excedidos, não é possivel mais sacar")
            elif ~se_excedeu_saques & se_excedeu_saldo:
                print("Saldo insuficiente, não possível sacar o valor")
            elif ~se_excedeu_saldo & ~se_excedeu_saques:
                saldo -= valor_saque
                extrato += f"Saque: R$ {valor_saque:.2f}\n"
                numero_saques += 1
                print("Saque realizado com sucesso")
                return(saldo,extrato)
            else:
                print("Erro na operação, o valor digitado é invalido!")
                return(saldo, extrato)
    else:
        print("Erro na operação, o valor digitado é invalido!")
        return(saldo, extrato)


def deposito(saldo, valor_deposito,extrato,/):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato = f"Depósito: R$ {valor_deposito:.2f}\n"
        print("Depósito realizado com sucesso")
        return(saldo, extrato)
    else:
        print("Erro na operação, o valor digitado é invalido!")
        return(saldo, extrato)
    

def gerar_extrato(saldo,/,*,extrato):
        
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")
        return

def criar_usuario(lista_usuarios):
    cpf = input("Digite seu CPF (Somente números):")
    if not cpf in lista_usuarios:
        nome = input("Digite seu nome:")
        data_nascimento = input("Digite sua data de nascimento(dd/mm/aaaa):")
        endereco = input("Digite seu endereço:")
        lista_usuarios[cpf] = {'nome':nome, 'data de nascimento': data_nascimento, 'endereço': endereco}
        print("Usuário criado com sucesso!")
        return lista_usuarios
    else:
        print("Já existe usuário com esse CPF")
        return lista_usuarios
    
def criar_conta(lista_usuarios, lista_contas):
    cpf = input("Digite seu CPF:")
    if cpf not in lista_usuarios:
        print("Não existe usuário com esse CPF")
        return lista_contas
    else:
        numero_conta = str(len(lista_contas)+1)
        lista_contas.append([cpf,numero_conta])
        print("Conta criada com sucesso!")
        return lista_contas
    
def listar_contas(lista_contas):
    if lista_contas == []:
        print("Não há contas cadastradas")
    else:
        print("Numero da conta")
        for conta in lista_contas:
            print(conta[1])
    return

def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    lista_usuarios = {}
    lista_contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor_deposito = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor_deposito, extrato)

        elif opcao == "s":
            valor_saque = float(input("Informe o valor do saque: "))
            saldo,extrato = saque(saldo = saldo, valor_saque= valor_saque, extrato = extrato, limite = limite, numero_saques= numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            gerar_extrato()

        elif opcao == "nu":
            lista_usuarios = criar_usuario(lista_usuarios)

        elif opcao == "nc":
            lista_contas = criar_conta(lista_usuarios, lista_contas)

        elif opcao == "q":
            print("Obrigado por usar nosso sistema")
            break

        elif opcao == "l":
            listar_contas(lista_contas)

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()