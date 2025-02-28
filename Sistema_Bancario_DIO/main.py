menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

==> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
i = 0

while True:
    
    opcao = input(menu)
    if opcao == "d":
        valor_deposito = float(input("Informe o valor do depósito: "))
            
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato = f"Depósito: R$ {valor_deposito:.2f}\n"
            print("Depósito realizado com sucesso")
        else:
            print("Erro na operação, o valor digitado é invalido!")
    
    elif opcao == "s":

        valor_saque = float(input("Informe o valor do saque: "))
        se_excedeu_saldo = True if valor_saque > saldo else False
        se_excedeu_saques = True if numero_saques >= LIMITE_SAQUES else False
        if valor_saque> 0:
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
            else:
                print("Erro na operação, o valor digitado é invalido!")
        else:
            print("Erro na operação, o valor digitado é invalido!")
    
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        print("Obrigado por usar nosso sistema")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")