import argparse, json, socket, pynput
from threading import Thread
from pynput import keyboard

from pynput.keyboard import HotKey

#argparser, receber opções pelo CLI
Parser = argparse.ArgumentParser(description="Control mouse & keyboard remotely")
Parser.version = "k1.0"

#arguments
Parser.add_argument('-ip',
                    type=str,
                    default='',
                    help='Concetion IP leave it blank if running the server')

Parser.add_argument('-p', '--port',
                    metavar='Port',
                    type=int,
                    default=50010,
                    help='connection Port')

Parser.add_argument('-s','--server',
                    action='store_true',
                    help='Runs the program in the server mode')

Parser.add_argument('-k', '--keyboard',
                    action='store_true',
                    help='Control Keyboard')

Parser.add_argument('-m',
                    '--mouse',
                    action='store_true',
                    help='Control Mouse')

Parser.add_argument('-l',
                    '--enable_local',
                    action='store_true',
                    help='Enable input device in both controled and local machines (only works for keyboard)')

# Parser.add_argument('-r', 
#                     '--reacts_to_monitor',
#                     action='store_true',
#                     help='Reacts to the position of the server monitor to change input from devices [T/R/B/L]')

args_CLI = Parser.parse_args()

class Client:
    def __init__(self, connection_ip, connection_port, keyboard_on=False, mouse_on=False, local_on=False):
        self.mouse_on = mouse_on
        self.keyboard_on = keyboard_on
        self.local_on = local_on

        # Verify if the code is being used for something
        assert mouse_on or keyboard_on == True, "You shouldn't use this code with mouse and keyboard turned off"

        # Start socket connection
        self.Socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket_obj.connect((connection_ip, connection_port))
        if self.keyboard_on:
            self.current_key = {'id': 1,
                                'key': None,
                                'pressed': False}

            #Opening keyboard listener
            self.keyboard_listener = pynput.keyboard.Listener(
                on_press = self.keyboard_on_press,
                on_release = self.keyboard_on_release,
                suppress = not local_on)

        # Keyboard controller, used in pause method
        self.keyboard = pynput.keyboard.Controller()

        if self.mouse_on:
            # Mouse information
            self.mouse = pynput.mouse.Controller()
            self.previousX, self.previousY = self.mouse.position

            # Opening mouse listeners 
            self.mouse_listener = pynput.mouse.Listener(
                on_move = self.mouse_on_move,
                on_scroll = self.mouse_on_scroll,
                on_click = self.mouse_on_click,
                suppress = not local_on,
            )

        # State control variables
        # Loop control 
        self.online = True

        # Pause control
        self.paused = False

        #Hotkeys listener
        self.Hotkeys_listener = pynput.keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+1': self.pause,
            '<ctrl>+<shift>+0': self.stop,
        })

    #===Keyboard Methods===#
    def keyboard_press(self, key, press):

        if key and self.keyboard_on: #filter none

            #Special Keys
            if type(key) == type(pynput.keyboard.Key.space): 
                key = str(key)
                self.current_key["id"] = 1.2
                self.send_key(key, press)

            #Alphanumeric keys
            elif key.char:
                key = key.char
                self.current_key["id"] = 1.1
                self.send_key(key, press)

            #Numpad Numbers
            elif 105 >= key.vk >= 96:
                key = str(key.vk - 96)
                self.current_key["id"] = 1.1
                self.send_key(key, press)

    #Send key via socket
    def send_key(self, key, press):
            self.current_key["key"] = key
            self.current_key["pressed"] = press
                
            self.Socket_obj.send(json.dumps(self.current_key).encode())

    #Callaction on press
    def keyboard_on_press(self, key):
        if not self.paused:
            self.keyboard_press(key, True)

    #Callaction on release
    def keyboard_on_release(self, key):
        if not self.paused:
            self.keyboard_press(key, False)

    #===Mouse methods===#
    def mouse_on_move(self, x, y):
        if not self.paused:
            if self.local_on:
                self.current_mouse = {'id': 2,
                                        'positionx': x - self.previousX,
                                        'positiony': y - self.previousY}

                self.previousX, self.previousY = x, y

            else:
                self.current_mouse = {'id': 2,
                                        'positionx': x - self.previousX,
                                        'positiony': y - self.previousY}

            self.Socket_obj.send(json.dumps(self.current_mouse).encode())

    def mouse_on_scroll(self, x, y , dx, dy):
        if not self.paused:
            self.current_mouse = {'id': 3,
                                'scrollx': dx,
                                'scrolly': dy}

            self.Socket_obj.send(json.dumps(self.current_mouse).encode())

    def mouse_on_click(self, x, y, button, pressed):
        if not self.paused:
            self.current_mouse = {'id': 4,
                                'click_button': str(button),
                                'pressed': pressed,
                                }

            self.Socket_obj.send(json.dumps(self.current_mouse).encode())

    # === EXECUTION === #
    def run(self):
        if self.mouse_on:
            self.mouse_listener.start()
        
        if self.keyboard_on:
            self.keyboard_listener.start()

        self.Hotkeys_listener.start()

        while self.online:
            if self.mouse_on == True and self.mouse_listener.is_alive() == False:
                break
            if self.keyboard_on == True and self.keyboard_listener.is_alive() == False:
                break
            
            pass

        self.Socket_obj.close()
        
        if self.mouse_on:
            self.mouse_listener.stop()
        
        if self.keyboard_on:
            self.keyboard_listener.stop()
    
    def stop(self):
        self.online = False

    def pause(self):
        # Toggle pause
        self.paused = not self.paused

        if self.paused:
            # Sending release commands to prevent from bugs
            self.current_key['id'] = 1.1
            self.current_key['key'] = '1'
            self.current_key['pressed'] = False
            self.Socket_obj.send(json.dumps(self.current_key).encode())
            self.current_key['id'] = 1.2
            self.current_key['key'] = 'Key.ctrl_l'
            self.Socket_obj.send(json.dumps(self.current_key).encode())
            self.current_key['key'] = 'Key.ctrl_r'
            self.Socket_obj.send(json.dumps(self.current_key).encode())
            self.current_key['key'] = 'Key.shift'
            self.Socket_obj.send(json.dumps(self.current_key).encode())

            # Stop suppress
            self.mouse_listener._suppress = False
            self.keyboard_listener._suppress = False
        else:
            # Sending release commands to prevent from bugs
            self.keyboard.release('1')
            self.keyboard.release(pynput.keyboard.Key.ctrl_l)
            self.keyboard.release(pynput.keyboard.Key.ctrl_r)
            self.keyboard.release(pynput.keyboard.Key.shift)

            # Restoring previous mouse position after retourning to suppress mode
            self.previousX, self.previousY = self.mouse.position

            # Activate suppress depending on user options
            self.mouse_listener._suppress = not self.local_on
            self.keyboard_listener._suppress = not self.local_on

#=== Server Class ===#
class Server:
    def __init__(self, port):
        self.keyboard = pynput.keyboard.Controller()
        self.mouse = pynput.mouse.Controller()

        #Socket connection, timeout defined to 10 sec
        self.Socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket_obj.bind(('', port))
        self.Socket_obj.listen(1)
        self.Socket_obj.settimeout(10)

        print("Searching connection...")

        self.connection, self.adress = self.Socket_obj.accept()
            
        print("Connected by:", self.adress)

        #Loop control variable
        self.online = True

    def run(self):

        while self.online:
            
            self.received_data = self.connection.recv(2048).decode()
            
            if self.received_data == "":
                break
            
            #cleaning data
            self.received_data = self.received_data.split("}")
            self.received_data.pop()

            for i in range( len(self.received_data) ):
                self.received_data[i] += "}"

                try:
                    self.received_data[i] = json.loads(self.received_data[i])
                    self.broken_package = False
                except:
                    self.broken_package = True

            if not self.broken_package:
        
                #Actions for each package
                for data in self.received_data:

                    # ===Keyboard data===
                    #Keyboard alphanumeric keys
                    if data['id'] == 1.1:
                        self.key = data['key']

                        if data['pressed']:
                            self.keyboard.press(self.key)

                        else:
                            self.keyboard.release(self.key)
                    
                    #Keyboard special keys
                    elif data['id'] == 1.2:

                        if data['pressed']:
                            exec("self.keyboard.press(pynput.keyboard." + data['key'] + ")")

                        else:
                            exec("self.keyboard.release(pynput.keyboard." + data['key'] + ")")

                    # ===Mouse data===
                    #Mouse movement
                    elif data['id'] == 2:
                        self.mouse.move(int(data['positionx']), int(data['positiony']))

                    #Mouse scroll
                    elif data['id'] == 3:
                        self.mouse.scroll(data['scrollx'], data['scrolly'])

                    #Mouse button press
                    elif data['id'] == 4:
                        
                        if data['pressed']:
                            exec("self.mouse.press(pynput.mouse." + data["click_button"] + ")")
                        else:
                            exec("self.mouse.release(pynput.mouse." + data["click_button"] + ")")
    
if args_CLI.server:
    server = Server(args_CLI.port)
    server.run()
else:
    client = Client(args_CLI.ip, args_CLI.port, keyboard_on=args_CLI.keyboard, mouse_on=args_CLI.mouse, local_on=args_CLI.enable_local)
    client.run()