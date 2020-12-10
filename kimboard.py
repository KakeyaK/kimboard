from tkinter import *
import os

pastaApp = os.path.dirname(__file__)

class KimboardGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Kimboard")
        self.master.minsize(500,500)
        # self.master.maxsize(500,500)
        
        # Frames

        self.portaeip = Frame(self.master)
        self.portaeip.pack(side = TOP, fill = BOTH)
        self.botoes = Frame(self.master)
        self.botoes.pack(side = TOP, expand = True)
        
        # Entradas de texto

        self.entry_ip = Label(self.portaeip, text="texto teste 1")
        self.entry_port = Label(self.portaeip, text="texto teste 2")

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

        self.console = Message(self.master, text="Aqui vai ser o console")

        # == Layout ==

        self.entry_ip.pack(side = LEFT)
        self.entry_port.pack(side = RIGHT)
        
        self.mouse_button.pack(side = LEFT, padx = 25)
        self.keyboard_button.pack(side = LEFT, padx = 25)
        self.keymouse_button.pack (side = LEFT, padx = 25)
        self.verbose_button.pack(side = LEFT, padx = 25)


root = Tk()
my_GUI = KimboardGUI(root)
root.mainloop()