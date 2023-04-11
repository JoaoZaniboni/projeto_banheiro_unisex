import threading

# Semáforos
lock_banheiro = threading.Semaphore(1)
lock_contagem_homens = threading.Semaphore(1)
lock_contagem_mulheres = threading.Semaphore(1)
max_funcionarios = 3
contagem_homens = 0
contagem_mulheres = 0

# Função para simular a entrada de um funcionário no banheiro
def usar_banheiro(genero_funcionario):
    global contagem_homens, contagem_mulheres
    if genero_funcionario == 'masculino':
        contagem_homens += 1
        print(f'Funcionário masculino entrou no banheiro. Total de homens no banheiro: {contagem_homens}')
    else:
        contagem_mulheres += 1
        print(f'Funcionária feminina entrou no banheiro. Total de mulheres no banheiro: {contagem_mulheres}')

# Função para simular a saída de um funcionário do banheiro
def sair_banheiro(genero_funcionario):
    global contagem_homens, contagem_mulheres
    if genero_funcionario == 'masculino':
        contagem_homens -= 1
        print(f'Funcionário masculino saiu do banheiro. Total de homens no banheiro: {contagem_homens}')
    else:
        contagem_mulheres -= 1
        print(f'Funcionária feminina saiu do banheiro. Total de mulheres no banheiro: {contagem_mulheres}')

# Função para funcionários do sexo masculino
def funcionario_masculino():
    while True:
        # Entrada no banheiro masculino
        lock_banheiro.acquire()
        lock_contagem_homens.acquire()
        if contagem_homens + contagem_mulheres < max_funcionarios:
            usar_banheiro('masculino')
            lock_contagem_homens.release()
            # Simula o tempo que o funcionário passa no banheiro
            # antes de sair
            threading.Event().wait(2)
            sair_banheiro('masculino')
            lock_banheiro.release()
            # Simula o tempo que o funcionário espera antes de tentar
            # entrar novamente no banheiro
            threading.Event().wait(3)
        else:
            lock_contagem_homens.release()
            lock_banheiro.release()
            # Simula o tempo que o funcionário espera quando o banheiro está
            # cheio
            threading.Event().wait(3)

# Função para funcionários do sexo feminino
def funcionario_feminino():
    while True:
        # Entrada no banheiro feminino
        lock_banheiro.acquire()
        lock_contagem_mulheres.acquire()
        if contagem_homens + contagem_mulheres < max_funcionarios:
            usar_banheiro('feminino')
            lock_contagem_mulheres.release()
            # Simula o tempo que a funcionária passa no banheiro
            # antes de sair
            threading.Event().wait(2)
            sair_banheiro('feminino')
            lock_banheiro.release()
            # Simula o tempo que a funcionária espera antes de tentar
            # entrar novamente no banheiro
            threading.Event().wait(3)
        else:
            lock_contagem_mulheres.release()
            lock_banheiro.release()
            
            # Simula o tempo que a funcionária espera quando o banheiro está
            # cheio
            threading.Event().wait(3)

# Inicializa as threads para os funcionários do sexo masculino e feminino
threading.Thread(target=funcionario_masculino).start()
threading.Thread(target=funcionario_feminino).start()