import socket
import threading

class Server:
    def __init__ (self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.clients = []
        self.usernames = []
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.initService()
        self.initConnections()
        
    def initService(self):
        self.server.bind((self.HOST,self.PORT))
        self.server.listen()
        print(f"> SERVIDOR < SERVIDOR ESTA ONLINE EM : {self.HOST}:{self.PORT}")
        
    def Broadcast(self, Message, clientSender=None):
        for client in self.clients:
            if(clientSender != self.usernames[self.clients.index(client)]):
                client.send(Message.encode('ascii'))
                print("SENDING BROADCAST")
    
    def LoadMessages(self, client):
        while True:
            print("in loadmessage")
            try:
                print("recebendo mensagem")
                getMsgFromClient = client.recv(2048).decode('ascii')
                CurrentUsername = self.usernames[self.clients.index(client)]                 
                self.Broadcast(f'> {self.usernames[self.clients.index(client)]} < {getMsgFromClient}',clientSender=CurrentUsername)
            except:
                leftClientIndex = self.clients.index(client)
                leftClientUsername = self.usernames[leftClientIndex]
                client.close()
                self.clients.remove(self.clients[leftClientIndex])
                self.usernames.remove(leftClientUsername)
                print(f"> SERVIDOR < {leftClientUsername} saiu do servidor")
                self.Broadcast(f"> SERVIDOR < {leftClientUsername} saiu do chat",)
        
    def initConnections(self):
        while True:
            client, address = self.server.accept()
            print(f"== [NOVA CONEXÃO] ==\nENDEREÇO : {address}")
            self.clients.append(client)
            client.send('GETUSER'.encode('ascii'))
            username = client.recv(2048).decode('ascii')
            print("recebendo user")
            self.usernames.append(username)
            self.Broadcast(f'> {username} < conectou-se ao chat')
            print("iniciando thread")
            self.client_thread = threading.Thread(target=self.LoadMessages,args=(client,))
            self.client_thread.start()
        
if __name__ == '__main__':
    print("WELCOME TO LOCALCHAT [SERVER - SIDE]")
    I_HOST, I_PORT = input('HOST: '), int(input('PORT: '))
    new_Server = Server(I_HOST,I_PORT)