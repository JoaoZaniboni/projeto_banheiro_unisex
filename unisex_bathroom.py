import threading
import time

# Semáforos para controlar o acesso ao banheiro e a contagem de funcionários
mutex = threading.Semaphore(1)
banheiro = []  # Lista para representar o banheiro

def usar_banheiro(sexo):
    print(f'Funcionário do sexo {sexo} entrou no banheiro')
    time.sleep(10)  # Simula o uso do banheiro por 2 segundos
    if sexo == 'feminino':
        banheiro.remove('F')
    else:
        banheiro.remove('M')
    print(f'Funcionário do sexo {sexo} saiu do banheiro')

def funcionario(sexo):
    while True:
        # Solicita ao usuário o próximo funcionário a entrar no banheiro
        entrada = input("Digite o próximo funcionário a entrar no banheiro (M para homem, F para mulher): ").upper()

        # Verifica a escolha do usuário e incrementa a contagem de homens ou mulheres
        if entrada == 'M':
            mutex.acquire()
            if 'F' not in banheiro and len(banheiro) < 3:  # Verifica se há menos de 3 homens no banheiro
                banheiro.append('M')  # Adiciona 'M' à lista de funcionários no banheiro
                mutex.release()
                usar_banheiro('masculino')
            else:
                mutex.release()
                print("Entrada de homem não permitida neste momento.")
        elif entrada == 'F':
            mutex.acquire()
            if 'M' not in banheiro and len(banheiro) < 3:  # Verifica se há menos de 3 mulheres no banheiro
                banheiro.append('F')  # Adiciona 'F' à lista de funcionários no banheiro
                mutex.release()
                usar_banheiro('feminino')
            else:
                mutex.release()
                print("Entrada de mulher não permitida neste momento.")
        else:
            print("Entrada inválida! Por favor, digite 'M' para homem ou 'F' para mulher.")

# Criação das threads para os funcionários
for i in range(2):
    t = threading.Thread(target=funcionario, args=('masculino',))
    t.start()

for i in range(2):
    t = threading.Thread(target=funcionario, args=('feminino',))
    t.start() 