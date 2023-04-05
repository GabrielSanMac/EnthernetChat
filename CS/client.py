import socket
import threading

class Client:
    def __init__(self,S_IP,S_PORT):
        self.S_IP = S_IP
        self.S_PORT = S_PORT
        self.username = ''
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection()
        self.getThread = threading.Thread(target=self.getMessage,args=())
        self.postThread = threading.Thread(target=self.postMessage,args=())
        #STARTING THREADS
        self.getThread.start()
        self.postThread.start()
        
    def getSrvInfo(self):
        self.S_IP = input('HOST: ')
        self.S_PORT = int(input('PORT: '))
        self.connection()
        
    def connection(self):
        try:
            self.client.connect((self.S_IP,self.S_PORT))
            print(f"> SERVIDOR < CONEXÃO ACEITA EM {self.S_IP}:{self.S_PORT} \n PARA CONTINUAR PRECISAMOS QUE SE IDENTIFIQUE COM UM USERNAME: ")
            self.username = input(">> USERNAME >> ")
        except:
            print("SERVIDOR NÃO ENCONTRADO TENTE NOVAMENTE OU ENTRE EM CONTATO COM O ADMINISTRADOR DO SERVIDOR.")
            self.getSrvInfo()
            
    def getMessage(self):
        while True:
            try:
                Message = self.client.recv(2048).decode('ascii')
                if Message == 'GETUSER':
                    self.client.send(self.username.encode('ascii'))
                else:
                    print(Message)
            except:
                print("> SERVIDOR STATUS < [OFFLINE]")
                break
    
    def postMessage(self):
        while True:
            try:
                Message = input("").encode('ascii')
                self.client.send(Message)
            except:
                print("SUA MENSAGEM AINDA NÃO E ACEITA PELO SERVIDOR, TENTE NÃO USAR ACENTOS NO ENVIO.")
            
            
if __name__ == '__main__':
    HOST,PORT = input("HOST: "),int(input("POST: "))
    chatClient = Client(HOST,PORT)