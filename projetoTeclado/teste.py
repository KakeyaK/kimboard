# from pynput import *
# import threading
# import time

#Vou tentar fazer aqui um leitor de listener de ambos os eventos de mouse e teclado
#Fazer dois pacotes diferentes para envio de dados

# current_key = {'id': 1,
#                'key': None,
#                'pressed': False}

# current_mouse = {'id': 2,
#                  'positionx': 0,
#                  'positiony': 0,
#                  'click_button': 0,
#                  'pressed': False,
#                  'scrollx': 0,
#                  'scrolly': 0}


# # class Data_Control (threading.Thread):
# #    def __init__(self):
# #       threading.Thread.__init__(self)
# #       self.ativo = True
   
# #    def run(self):
# #         while(self.ativo):
# #             print(current_key)
# #             time.sleep(0.01)

# def keyboard_on_press(key):
#     global current_key
#     current_key["key"] = str(key)
#     current_key["pressed"] = True
#     print(current_key)

# def keyboard_on_release(key):
#     global current_key
#     current_key["key"] = str(key)
#     current_key["pressed"] = False
#     print(current_key)


# keyboard_l = keyboard.Listener(
#     on_press=keyboard_on_press,
#     on_release=keyboard_on_release)

# def mouse_on_move(x, y):
#     global current_mouse
#     current_mouse['positionx'] = x
#     current_mouse['positiony'] = y
    
#     if(current_mouse['pressed'] == False):
#         current_mouse['click_button'] = None
        
#     print(current_mouse)

# def mouse_on_scroll(x, y , dx, dy):
#     global current_key
#     current_mouse['scrollx'] = dx
#     current_mouse['scrolly'] = dy

#     if(current_mouse['pressed'] == False):
#         current_mouse['click_button'] = None

#     print(current_mouse)

# def mouse_on_click(x, y, button, pressed):
#     global current_mouse
    
#     current_mouse['click_button'] = button
#     current_mouse['pressed'] = pressed

#     print(current_mouse)


# mouse_l = mouse.Listener(
#     on_move = mouse_on_move,
#     on_scroll = mouse_on_scroll,
#     on_click = mouse_on_click
# )

# mouse_l.start()
# keyboard_l.start()

# while(1):
#     pass





# import ctypes

# ctypes.windll.shcore.SetProcessDpiAwareness(2)

# screensize = ctypes.windll.user32.GetSystemMetrics(78), ctypes.windll.user32.GetSystemMetrics(79)

# ####LEMBRAR DE QUE O CLIENT PODE TER DOIS MONITORES

# print(screensize)


# def on_move(x, y):
#     print('Pointer moved to {0}'.format(
#         (x, y)))
#     if x >= screensize[0]:
#         print("chegou na borda direita!")
#         return False
#     elif x <= 0:
#         print("chegou na borda esquerda!")
        
#     elif y <= 0:
#         print("chegou na borda de cima!")
#         return False
#     elif y >= screensize[1]:
#         print("chegou na borda de baixo!")
#         return False

# with mouse.Listener(on_move=on_move) as listener:
#     listener.join()


import argparse

#argparser
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
                    #  metavar='server',
                     action='store_true',
                     help='Runs the program in the server mode')
parser0.add_argument('-k',
                     '--keyboard',
                    #  metavar='use_keyboard',
                     action='store_true',
                     help='Control Keyboard')
parser0.add_argument('-m',
                     '--mouse',
                    #  metavar='use_mouse',
                     action='store_true',
                     help='Control Mouse')
parser0.add_argument('-l',
                     '--local',
                    #  metavar='use_local',
                     action='store_true',
                     help='Enable input device in both controled and local machines')

parser0.add_argument('-r', 
                     '--reacts_to_monitor',
                    #  metavar='react_to_monitor',
                     action='store',
                     help='Reacts to the position of the server monitor to change input from devices [T/R/B/L]')

args = parser0.parse_args()

print(args.conection_port)