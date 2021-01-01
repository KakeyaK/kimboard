from socket import *
from pynput import *
import json

ativo = True

serverHost = 'localhost'
serverPort = 50007
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

current_key = {'id': 1,
               'key': None,
               'pressed': False}

current_mouse = {'id': 2,
                 'positionx': 0,
                 'positiony': 0,
                 'click_button': 0,
                 'pressed': False,
                 'scrollx': 0,
                 'scrolly': 0}

def keyboard_on_press(key):
    global ativo

    if key == keyboard.Key.esc:
        # Stop listener
        ativo = False

    global current_key
    current_key["key"] = str(key)
    current_key["pressed"] = True
    
    sockobj.send(json.dumps(current_key).encode())

def keyboard_on_release(key):
    global current_key
    current_key["key"] = str(key)
    current_key["pressed"] = False
    
    sockobj.send(json.dumps(current_key).encode())


keyboard_l = keyboard.Listener(
    on_press=keyboard_on_press,
    on_release=keyboard_on_release)

def mouse_on_move(x, y):
    global current_mouse

    current_mouse['id'] = 2
    
    current_mouse['scrollx'] = 0
    current_mouse['scrolly'] = 0
    
    current_mouse['positionx'] = x
    current_mouse['positiony'] = y
    
    if(current_mouse['pressed'] == False):
        current_mouse['click_button'] = None
        
    sockobj.send(json.dumps(current_mouse).encode())

def mouse_on_scroll(x, y , dx, dy):
    global current_mouse

    current_mouse['id'] = 3

    current_mouse['scrollx'] = dx
    current_mouse['scrolly'] = dy

    if(current_mouse['pressed'] == False):
        current_mouse['click_button'] = None

    sockobj.send(json.dumps(current_mouse).encode())

def mouse_on_click(x, y, button, pressed):
    global current_mouse

    current_mouse['id'] = 4
    
    current_mouse['scrollx'] = 0
    current_mouse['scrolly'] = 0

    current_mouse['click_button'] = str(button)
    current_mouse['pressed'] = pressed

    sockobj.send(json.dumps(current_mouse).encode())


mouse_l = mouse.Listener(
    on_move = mouse_on_move,
    on_scroll = mouse_on_scroll,
    on_click = mouse_on_click
)

keyboard_l.start()
mouse_l.start()

while ativo:
    pass

sockobj.close()
