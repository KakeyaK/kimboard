from tkinter import *
import os

from socket import *
from pynput import keyboard

pastaApp = os.path.dirname(__file__)

class Kimboard_Client:
    def __init__(self, ip, port):
        self.client_ip = ip
        self.client_port = port
        self.sockobj = socket(AF_INET, SOCK_STREAM)

    def conectar(self):
        self.sockobj.connect((self.client_ip, self.client_port))

    def enviar_teclado(self, key):
        self.msg = str(key)
        self.sockobj.send(self.msg.encode())

    def ligar_teclado(self):
        with keyboard.Listener(
            on_press=self.enviar_teclado
        ) as listener:
        
            listener.join()
    
    def desligar_teclado(self):
        self.sockobj.close()
        #desligar listener

class Kimboard_Server:
    def __init__(self, port):
        self.server_ip = 'localhost'
        self.server_port = port
        self.sockobj = socket(AF_INET, SOCK_STREAM)

    def conectar(self):
        self.sockobj.bind((self.server_ip, self.server_port))
        self.sockobj.listen(5)

    def ligar_servidor(self):
        
        self.conexao, self.endereco = self.sockobj.accept()
        print('Conectado por, ', self.endereco)

        while True:
            self.data = conexao.recv(1024)
            if data.decode() == '':
                print('data retrieved was nothing')
                break
            print('recebido:', data.decode())
            
#======== GUI ========#

class KimboardGUI_Initial_Screen:

    def __init__(self, master):
        self.master = master
        self.master.title("Escolha o Modo de Funcionamento")
        self.master.geometry("400x200")

        #botões
        self.server_button = Button(self.master, text = "Servidor", font = "helvetica, 16", command = lambda: self.abrir_servidor())
        self.server_button.pack(side = LEFT, padx = 40)
        
        self.client_button = Button(self.master, text = "Cliente", font = "helvetica, 16", command = lambda: self.abrir_cliente())
        self.client_button.pack(side = RIGHT, padx = 40)

    #funções dos botões

    def abrir_servidor(self):
        print("hello world")
        # self.win = Toplevel(self.master)
        # KimboardGUI_Server(self.win)
        
    def abrir_cliente(self):
        print("hello world")
        # self.win = Toplevel(self.master)
        # KimboardGUI_Client(self.win)

class KimboardGUI_Server:

    def __init__(self, master):
        self.master = master
        self.master.title("Servidor")
        self.master.geometry("200x200")

        #variável

        self.informacao = StringVar()
        self.informacao.set("Aguardando conexão")

        #label

        self.exibir_informacao = Label(master, textvariable = self.informacao, font = "helvetica, 13")
        self.exibir_informacao.pack(side = LEFT, fill= BOTH, expand= True)

class KimboardGUI_Client:

    def __init__(self, master):
        self.master = master
        self.master.title("Kimboard")
        self.master.minsize(850,600)
        self.master.maxsize(850,600)

        #variáveis

        self.texto_console = StringVar()
        self.texto_console.set("Nada para mostrar por enquanto")

        self.ip = StringVar()
        self.port = StringVar()
    
        # Frames

        self.portaeip = Frame(self.master)
        self.portaeip.pack(side = TOP, fill = BOTH)

        self.portaeip_entry = Frame(self.master)
        self.portaeip_entry.pack(side = TOP, fill = BOTH)

        self.botoes = Frame(self.master)
        self.botoes.pack(side = TOP, pady=(100, 100))
        
        self.console_frame = Frame(self.master)
        self.console_frame.pack(side = TOP, expand = True, fill = BOTH)
        self.console_frame.configure(background = "black")
        
        # Entradas de texto

        #ip
        self.label_ip = Label(self.portaeip, text="Insira o IP", padx = (55), pady = (20), font="helvetica, 14")
        self.entry_ip = Entry(self.portaeip_entry, textvariable = self.ip, font="helvetica, 14")

        #porta
        self.label_port = Label(self.portaeip, text="Insira a porta", padx = (155), pady = (20), font="helvetica, 14")
        self.entry_port = Entry(self.portaeip_entry, textvariable = self.port, font="helvetica, 14")

        # Botões
        self.mouse_img = PhotoImage(file =pastaApp+"\\MouseButton.gif")
        self.mouse_button = Button(self.botoes, image = self.mouse_img, borderwidth = 0)
        self.mouse_button.image = self.mouse_img

        self.keyboard_img = PhotoImage(file = pastaApp+"\\KeyboardButton.gif")
        self.keyboard_button = Button(self.botoes, image = self.keyboard_img, borderwidth = 0)
        self.keyboard_button.image = self.keyboard_img

        self.keymouse_img = PhotoImage(file = pastaApp+"\\KeymouseButton.gif")
        self.keymouse_button = Button(self.botoes, image = self.keymouse_img, borderwidth = 0)
        self.keymouse_button.image = self.keymouse_img

        self.verbose_img = PhotoImage(file = pastaApp+"\\VerboseButton.gif")
        self.verbose_button = Button(self.botoes, image = self.verbose_img, borderwidth = 0)
        self.verbose_img.image = self.verbose_img

        # Console

        self.console = Message(self.console_frame, width=800, justify="left", anchor = W, textvariable = self.texto_console)
        self.console.config( fg="white", font=('Helvetica', 14), bg="black")

        # == Layout ==

        self.label_ip.pack(side = LEFT)
        self.label_port.pack(side = RIGHT)

        self.entry_ip.pack(side = LEFT, padx = 55)
        self.entry_port.pack(side = RIGHT, padx = 45)
        
        self.mouse_button.pack(side = LEFT, padx = 25)
        self.keyboard_button.pack(side = LEFT, padx = 25)
        self.keymouse_button.pack (side = LEFT, padx = 25)
        self.verbose_button.pack(side = LEFT, padx = 25)
        self.console.pack(side = TOP, fill = X)

        #início para escolha entre cliente ou servidor
        
        self.win = Toplevel(self.master)
        KimboardGUI_Initial_Screen(self.win)


root = Tk()
my_GUI = KimboardGUI_Client(root)
root.mainloop()