from socket import *
from pynput.keyboard import Key, Controller

keyboard = Controller()


meuHost = 'localhost'
minhaPort = 50007
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((meuHost, minhaPort))
sockobj.listen(1)

ativo = True

while ativo:
    conexão, endereço = sockobj.accept()
    print('Conectado por', endereço)
    
    while True:
        data = conexão.recv(1024)
        if data.decode() == "":
            break
        print("recebido:", data.decode( ))
        #código para executar o que foi enviado
        #keyboard.press(data.decode())
        #keyboard.release(data.decode())

    conexão.close()
    break
