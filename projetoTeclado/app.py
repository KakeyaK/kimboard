from pynput import *

import argparse
import json
import socket

#argparser, receber opções pelo CLI
parser0 = argparse.ArgumentParser(description="Control mouse & keyboard remotely")
parser0.version = "k1.0"

#positional arguments
parser0.add_argument('concetion_iP',
                     metavar='Ip',
                     type=str,
                     default='',
                     help='Concetion IP if running the server leave it blank ("")')
parser0.add_argument('conection_port',
                     metavar='Port',
                     type=str,
                     help='Conection Port')

#optional arguments
parser0.add_argument('-s',
                     '--server',
                     action='store_true',
                     help='Runs the program in the server mode')
parser0.add_argument('-k',
                     '--keyboard',
                     action='store_true',
                     help='Control Keyboard')
parser0.add_argument('-m',
                     '--mouse',
                     action='store_true',
                     help='Control Mouse')
parser0.add_argument('-l',
                     '--local',
                     action='store_true',
                     help='Enable input device in both controled and local machines')
parser0.add_argument('-r', 
                     '--reacts_to_monitor',
                     action='store',
                     help='Reacts to the position of the server monitor to change input from devices [T/R/B/L]')

args_CLI = parser0.parse_args()

#====SERVIDOR====#
class Servidor:
    def __intit__(self, port):
        #Iniciando controlador e variáveis do teclado
        self.controle_teclado = keyboard.Controller()
        self.tecla_anterior = ""

        #Iniciando controlador e variáveis do mouse
        self.controle_mouse = mouse.Controller()
        self.mousex_anterior = 0
        self.mousey_anterior = 0

        #Iniciando configuração do socket
        self.meuHost = ''
        self.minhaPort = port
        self.sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockobj.bind((self.meuHost, self.minhaPort))
        self.sockobj.listen(1)

        #Main
        print("Vou procurar a conexão")
        self.conexao, self.endereço = self.sockobj.accept()
        print('Conectado por', self.endereço, '\n')

        while True:
            self.data = self.conexao.recv(2048).decode()
            if self.data == "":
                break
            
            self.read_data = json.loads(self.data)

            #recebendo dados do teclado
            if self.read_data['id'] == 1:
                if self.read_data['pressed']:
                    exec("self.controle_teclado.press(" + self.read_data['key'] +")")
                else:
                    exec("self.controle_teclado.release(" + self.read_data['key'] +")")
                
            #recebendo dados do mouse
            elif self.read_data['id'] > 1:

                #movimento do mouse
                if self.read_data['id'] == 2:

                    #cuidado com possível erro por alcançar limites da tela
                    self.controle_mouse.move(self.read_data['positionx'] - self.mousex_anterior, self.read_data['positiony'] - self.mousey_anterior)

                    self.mousex_anterior = self.read_data['positionx']
                    self.mousey_anterior = self.read_data['positiony']

                #scroll do mouse
                if self.read_data['id'] == 3:

                    #verificar necessidade de gerar excessão
                    self.controle_mouse.scroll(self.read_data['scrollx'], self.read_data['scrolly'])

                #click do mouse
                if self.read_data['id'] == 4:

                    if self.read_data['pressed']:
                        exec("self.controle_mouse.press(" + self.read_data["click_button"] + ")")
                    else:
                        exec("self.controle_mouse.release(" + self.read_data["click_button"] + ")")

            #verificação dos dados recebidos                
            # print("recebido:", data)


#====CLIENTE====#
class Cliente:
    def __init__(self, ip, port, usekeyboard, usemouse, use_local, react_to_monitor):

        self.ativo = True

        self.severIP = ip
        self.serverPort = port
        self.sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockobj.connect((self.severIP, self.serverPort))

        self.current_key = {'id': 1,
                    'key': None,
                    'pressed': False}

        self.current_mouse = {'id': 2,
                        'positionx': 0,
                        'positiony': 0,
                        'click_button': 0,
                        'pressed': False,
                        'scrollx': 0,
                        'scrolly': 0}

        if usekeyboard:
            self.keyboard_l = keyboard.Listener(
                on_press=self.keyboard_on_press,
                on_release=self.keyboard_on_release,
                suppress=not use_local
            )

            self.keyboard_l.start()

        if usemouse:

            self.mouse_l = mouse.Listener(
                on_move = self.mouse_on_move,
                on_scroll = self.mouse_on_scroll,
                on_click = self.mouse_on_click,
                suppress=not use_local
            )

            self.mouse_l.start()


        while self.ativo:
            pass

        self.sockobj.close()


    def keyboard_on_press(self, key):

        if key == keyboard.Key.esc:
            # Stop listener
            self.ativo = False

        self.current_key["key"] = str(key)
        self.current_key["pressed"] = True
        
        self.sockobj.send(json.dumps(self.current_key).encode())

    def keyboard_on_release(self, key):
        
        self.current_key["key"] = str(key)
        self.current_key["pressed"] = False
        
        self.sockobj.send(json.dumps(self.current_key).encode())

    def mouse_on_move(self, x, y):
        self.current_mouse['id'] = 2
        
        self.current_mouse['scrollx'] = 0
        self.current_mouse['scrolly'] = 0
        
        self.current_mouse['positionx'] = x
        self.current_mouse['positiony'] = y
        
        if(self.current_mouse['pressed'] == False):
            self.current_mouse['click_button'] = None
            
        self.sockobj.send(json.dumps(self.current_mouse).encode())

    def mouse_on_scroll(self, x, y , dx, dy):
        
        self.current_mouse['id'] = 3

        self.current_mouse['scrollx'] = dx
        self.current_mouse['scrolly'] = dy

        if(self.current_mouse['pressed'] == False):
            self.current_mouse['click_button'] = None

        self.sockobj.send(json.dumps(self.current_mouse).encode())

    def mouse_on_click(self, x, y, button, pressed):
        self.current_mouse['id'] = 4
        
        self.current_mouse['scrollx'] = 0
        self.current_mouse['scrolly'] = 0

        self.current_mouse['click_button'] = str(button)
        self.current_mouse['pressed'] = pressed

        self.sockobj.send(json.dumps(self.current_mouse).encode())


