import threading
from time import sleep
from random import randint, choice


class funcionario:
    def __init__(self, sexo):
        self.sexo = sexo
        self.iniciar()

    def iniciar(self):

        id_thread = threading.get_ident()
        
        self.entrar_banheiro()
        print(f"Cliente {self.sexo} {id_thread} ENTROU no banheiro")

        sleep(randint(1,5))                         # "dorme"

        self.sair_banheiro()
        print(f"Cliente {self.sexo} {id_thread} SAIU do banheiro")


    def entrar_banheiro(self):
        if self.sexo == "M":
            maximo_m.acquire()                      # impede mais de 3 entrarem
            global m

            mutexM.acquire()                        # mutex para acessar variavel que conta quantas pessoas tem

            if m == 0:                              # se n tiver ninguem do mesmo sexo, tenta adquirir exclusividade do banheiro
                ocupado.acquire()                   # (se outro sexo ja estiver dentro nao vai conseguir adquirir ate ele esvaziar) - semaforo binario

            m += 1                                  # + uma pessoa dentro

            mutexM.release()

        else:
            maximo_f.acquire()                      # semaforo impede mais de 3 entrarem
            global f                    
            
            mutexF.acquire()                        # mutex para acessar variavel que conta quantas pessoas tem

            if f == 0:                              # se n tiver ninguem do mesmo sexo, tenta adquirir exclusividade do banheiro
                ocupado.acquire()                   # (se outro sexo ja estiver dentro nao vai conseguir adquirir ate ele esvaziar) - semaforo binario
            
            f += 1                                  # + uma pessoa dentro

            mutexF.release()

    def sair_banheiro(self):
        if self.sexo == "M":
            maximo_m.release()                      # impede mais de 3 entrarem
            global m

            mutexM.acquire()                        # mutex para acessar variavel que conta quantas pessoas tem

            m -= 1                                  # + uma pessoa dentro

            if m == 0:
                ocupado.release()                   # libera semaforo para que outro sexo pegue a exclusividade

            mutexM.release()

        else:
            maximo_f.release()                      # impede mais de 3 entrarem
            global f

            mutexF.acquire()                        # mutex para acessar variavel que conta quantas pessoas tem
            
            f -= 1                                  # + uma pessoa dentro

            if f == 0:
                ocupado.release()                   # libera semaforo para que outro sexo pegue a exclusividade

            mutexF.release()


# n_thread, tamanho_banheiro = [int(x) for x in input("Digite o número de threads (pessoas) e o tamanho do banheiro").split()]
n_thread = 10
tamanho_banheiro = 3

ocupado = threading.Semaphore(1)        # garante 1 sexo por vez

m = 0
f = 0

mutexM = threading.Lock()
mutexF = threading.Lock()

maximo_m = threading.Semaphore(tamanho_banheiro)
maximo_f = threading.Semaphore(tamanho_banheiro)


for n in range(n_thread // 2):                              # metade
    t = threading.Thread(target=funcionario, args=('M'))
    t.start()

for n in range(n_thread % 2 + n_thread // 2):               # metade ou metade + 1 para impar
    t = threading.Thread(target=funcionario, args=('F'))
    t.start()

# for n in range(n_thread):                             # metade
#     i = randint(1,10)
#     if i > 5:
#         t = threading.Thread(target=funcionario, args=('M'))
#     else:                                          
#         t = threading.Thread(target=funcionario, args=('F'))
#     t.start()


#for n in range(n_thread):                              # metade
#    t = threading.Thread(target=funcionario, args=(choice(["M", "F"])))
#    t.start()
