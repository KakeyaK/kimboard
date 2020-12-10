from socket import *

#Client side

def conectar_client(ipv4, port):

    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((ipv4, port))

def enviar_msg(msg):

    sockobj.send(msg.enconde())

#Server side

def conectar_server(ipv4, port, ndispositivos):
    
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind((ipv4,port))
    sockobj.listen(ndispositivos)

    conexao, endereco = sockobj.accept()
    return (conexao, endereco)

def receber_msg(conexao):

    return conexao.recv(1024)

def desconectar_server(conexao):
    conexao.close()

def desconectar_client():
    sockobj.close()


