
# criar interface cli - ok

# criar controle de mouse sem gui
#     -detectar tamanho da tela - ok
#     -detectar quando o mouse encostar na borda da tela - ok
    # -passar informações do mouse pelo client
    # -receber informações do mouse no server e mover conforme necessário
    # -configurar mouse para trocar quando enconstar na borda

# criar teclas de comando para o teclado
# aprender a parar o mouse e teclado locais

# tratar informações do cli

#===CLI===

#argumentos que eu preciso receber
# Fixos:
# -ip
# -porta


# Opcionais:
# -teclado sim ou não
# -mouse sim ou não
# -cancelar local sim ou nao

import json
import argparse
from socket import *  #converter isso daqui pro outro método depois acho que é melhor
from pynput.keyboard import Key, Controller

#argparser
# parser0 = argparse.ArgumentParser(description="Control mouse & keyboard remotely")
# parser0.version = "k1.0"

# #positional arguments
# parser0.add_argument('Concetion IP',
#                      metavar='IP',
#                      type=str,
#                      default='',
#                      help='Concetion IP if running the server leave it blank ("")')
# parser0.add_argument('Conection Port',
#                      metavar='Port',
#                      type=str,
#                      help='Conection Port')

# #optional arguments
# parser0.add_argument('-s',
#                      '--server',
#                      action='store_true',
#                      help='Runs the program in the server mode')
# parser0.add_argument('-k',
#                      '--keyboard',
#                      action='store_true',
#                      help='Control Keyboard')
# parser0.add_argument('-m',
#                      '--mouse',
#                      action='store_true',
#                      help='Control Mouse')
# parser0.add_argument('-l',
#                      '--local',
#                      action='store_true',
#                      help='Enable input device in both controled and local machines')
# parser0.add_argument('-server_monitor',
#                      '--server_monitor',
#                      action='store',
#                      help='Reacts to the position of the server monitor when changing mouse from devices')

#keyboard
keyboard = Controller()
tecla_anterior = ""

#socket
meuHost = ''
minhaPort = 50007
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((meuHost, minhaPort))
sockobj.listen(1)


#main
print("vou procurar")
conexão, endereço = sockobj.accept()
print('Conectado por', endereço, '\n')

while True:
    data = conexão.recv(2048).decode()
    if data == "":
        break
    
    # read_data = json.loads(data)

    # #recebendo dados do teclado
    # if read_data['id'] == 1:
    #     if read_data['']
        
    # #recebendo dados do mouse
    # if read_data['id'] == 2:
        
    print("recebido:", data)


    # if tecla != tecla_anterior:
        #código para executar o que foi enviado
        # exec("keyboard.press(" + tecla +")")
        # exec("keyboard.release(" + tecla +")")

    # tecla_anterior = tecla

conexão.close()
