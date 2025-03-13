from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []
        pass

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self,conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, numero_conta,cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        pass
    
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero_conta(self):
        return self._numero_conta
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def saque(self, valor_saque):

        saldo = self._saldo

        se_excedeu_saldo = valor_saque > saldo

        if valor_saque> 0:
            if se_excedeu_saldo:
                print("Saldo insuficiente, não foi possível realizar a operação ")
                return False
            else:
                self._saldo -= valor_saque
                print("Saque realizado com sucesso")
                return True
        else:
            print("Erro na operação, o valor digitado é invalido!")
            return False
    
    def deposito(self, valor_deposito):
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print("Depósito realizado com sucesso")
            return True
        else:
            print("Erro na operação, o valor digitado é invalido!")
            return False
        


class Conta_corrente(Conta):
    def __init__(self, numero_conta, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        pass

    def saque(self, valor_saque):

        saques_realizados = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        limite = self.limite
        limite_saques = self.limite_saques

        se_excedeu_limite = valor_saque > limite
        se_excedeu_saques = saques_realizados > limite_saques


        if valor_saque> 0:
            if se_excedeu_limite:
                print("Limite insuficiente, não foi possível realizar a operação")
            elif se_excedeu_saques:
                print("Quantidade de saques excedido, não foi possível realizar a operação")
            else:
                return super().saque(valor_saque)
        else:
            print("Erro na operação, o valor digitado é invalido!")
        
        return False
        
    def __str__(self):
        return f"""\
            Agência:\t {self.agencia}
            C\C: \t\t{self.numero_conta}
            Titular: \t{self.cliente.nome}
        """

class Historico():
    def __init__(self):
        self._transacoes = []
        pass

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.saque(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.deposito(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Pessoa_fisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        pass




def menu():
    menu = """

        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        [nu] Cadastrar novo cliente
        [nc] Criar nova conta
        [l] Listar contas

    ==> """
    opcao = input(menu)
    return opcao


def filtrar_lista_usuarios(cpf,lista_usuarios):
    lista_filtrada = [usuario for usuario in lista_usuarios if usuario.cpf == cpf]
    return lista_filtrada[0] if lista_filtrada else None

def filtrar_lista_contas(usuario):
    if not usuario.contas:
        print("O cliente não possui contas cadastradas")
        return
    lista_contas_cpf = [str(conta.numero_conta) for conta in usuario.contas]
    conta_valida = False
    while not conta_valida:
        conta_selecionada_str = input("Você possui as seguintes contas: \n" +
            "".join(str(conta.numero_conta) + "\n" for conta in usuario.contas) +
            "Selecione a conta desejada \n" +
            "===>"
            )

        if str(conta_selecionada_str) in lista_contas_cpf:
            conta_selecionada = [conta for conta in usuario.contas if conta.numero_conta == int(conta_selecionada_str)]
            conta_valida = True
        elif conta_selecionada_str == "q":
            return False
        else:
            print("Conta selecionada é invalida, digite novamente ou digite q para cancelar a operação\n\n")

    return conta_selecionada[0]
    


def depositar(lista_usuarios):
    cpf = input("Digite o seu CPF: ")
    usuario = filtrar_lista_usuarios(cpf,lista_usuarios)
    if not usuario:
        print("CPF Inválido! O Usuario não foi cadastrado!")
        return
    valor_deposito = float(input("Digite o valor desejado para deposito: "))
    transacao = Deposito(valor_deposito)
    conta_selecionada = filtrar_lista_contas(usuario)
    if not conta_selecionada:
        return print("Operacao cancelada")
    usuario.realizar_transacao(conta_selecionada, transacao)

def sacar(lista_usuarios):
    cpf = input("Digite o seu CPF: ")
    usuario = filtrar_lista_usuarios(cpf,lista_usuarios)
    if not usuario:
        print("CPF Inválido! O Usuario não foi cadastrado!")
        return
    valor_saque = float(input("Digite o valor desejado para saque: "))
    transacao = Saque(valor_saque)
    conta_selecionada = filtrar_lista_contas(usuario)
    if not conta_selecionada:
        return print("Operacao cancelada")
    usuario.realizar_transacao(conta_selecionada, transacao)

def gerar_extrato(lista_usuarios):
        
    cpf = input("Digite o seu CPF: ")
    usuario = filtrar_lista_usuarios(cpf,lista_usuarios)
    if not usuario:
        print("CPF Inválido! O Usuario não foi cadastrado!")
        return
    conta_selecionada = filtrar_lista_contas(usuario)
    if not conta_selecionada:
        return print("Operacao cancelada")

    print("\n================ EXTRATO ================")
    transacoes = conta_selecionada.historico.transacoes

    extrato = ""

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo: R$ {conta_selecionada.saldo:.2f}")
    print("==========================================")
    return

def criar_conta(lista_usuarios, lista_contas, numero_conta):
    cpf = input("Digite o seu CPF: ")
    usuario = filtrar_lista_usuarios(cpf,lista_usuarios)
    if not usuario:
        print("CPF Inválido! O Usuario não foi cadastrado!")
        return
    conta = Conta_corrente.nova_conta(cliente= usuario, numero = numero_conta)
    lista_contas.append(conta)
    usuario.contas.append(conta)

    print("Conta criada com sucesso!")
    
def criar_usuario(lista_usuarios):
    cpf = input("Digite o seu CPF: ")
    usuario = filtrar_lista_usuarios(cpf,lista_usuarios)
    if usuario:
        print("Já existe um usuário com esse cpf")
        return
    nome = input("Digite seu nome:")
    data_nascimento = input("Digite sua data de nascimento(dd/mm/aaaa):")
    endereco = input("Digite seu endereço:")

    usuario = Pessoa_fisica(cpf = cpf, nome = nome, data_nascimento=data_nascimento, endereco=endereco)
    lista_usuarios.append(usuario)
    print("Usuário criado com sucesso!")
    

def listar_contas(lista_contas):
    for conta in lista_contas:
        print(textwrap.dedent(str(conta)))

def main():

    lista_usuarios = []
    lista_contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(lista_usuarios)

        elif opcao == "s":
            sacar(lista_usuarios)
            

        elif opcao == "e":
            gerar_extrato(lista_usuarios)

        elif opcao == "nu":
            criar_usuario(lista_usuarios)

        elif opcao == "nc":
            numero_conta = len(lista_contas)+1
            criar_conta(lista_usuarios, lista_contas, numero_conta)

        elif opcao == "q":
            print("Obrigado por usar nosso sistema")
            break

        elif opcao == "l":
            listar_contas(lista_contas)

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()