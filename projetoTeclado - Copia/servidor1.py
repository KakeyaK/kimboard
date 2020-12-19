from socket import *
from pynput.keyboard import Key, Controller

keyboard = Controller()


meuHost = ''
minhaPort = 50007
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((meuHost, minhaPort))
sockobj.listen(1)

# ativo = True

# while ativo:
print("vou procurar")
conexão, endereço = sockobj.accept()
print('Conectado por', endereço)

while True:
    print("estou rodando")
    data = conexão.recv(1024)
    if data.decode() == "":
        break
    print("recebido:", data.decode( ))
    tecla = data.decode()
    print(tecla[1])
    #código para executar o que foi enviado
    keyboard.press(tecla[1])
    keyboard.release(tecla[1])

conexão.close()
