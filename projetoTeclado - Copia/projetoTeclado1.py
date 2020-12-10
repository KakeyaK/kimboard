import sys
import argparse
from socket import *

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def conectar():
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.connect((self.ip, self.port))


class Server:
    def __init__(self, ip, port, ndevices):
        self.ip = ip
        self.port = port
        self.ndevices = ndevices

    def conectar():
        self.sockobj = socket(AF_INET, SOCK_STREAM)
        self.sockobj.bind((self.ip, self.port))
        self.sockobj.listen(ndevices)





def main():
    parser = argparse.ArgumentParser(description='argumentos para exeussão do programa')
    parser.add_argument('--ip', required=True)
    parser.add_argument('--port', required=True, default=50001)
    
    args = parser.parse_args()
     
    ##print("Intervalo= {}".format(args.intervalo))
 
if __name__ == '__main__':
    sys.exit(main())