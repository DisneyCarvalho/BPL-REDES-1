import socket
import threading
import json

class Broker:
    def __init__(self, tcp_port, udp_port,ip):
        #Portas tcp/udp
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        

        #Ip do server
        self.address = ip

        #thred tcp/udp
        self.tcp_thread = threading.Thread(target=self.tcp_server)
        self.udp_thread = threading.Thread(target=self.udp_server)
        self.udp_thread.daemon = True
        self.tcp_thread.daemon = True


        self.dispositivos = {}

    def start(self):
        self.dispositivos = {}

        #Incia as threads
        self.tcp_thread.start()
        self.udp_thread.start()

    def tcp_server(self):
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((self.address, self.tcp_port))
        tcp_server.listen(3)
        print(f"TCP Server {self.tcp_port}")

        while True:
            client_socket, addr = tcp_server.accept()
            client_socket.settimeout(5)
            print(f"TCP connection {addr}")
            threading.Thread(target=self.tcp_client, args=(client_socket,addr,)).start()


    def tcp_client(self, client_socket,addr):
        data = None
        while True:
            try:
                data = client_socket.recv(1024)
                try:
                    rec = json.loads(data)
                except:
                    rec = {}

                self.buton(rec)

            except ConnectionAbortedError:
                break
            except TimeoutError:
                break
            except ConnectionResetError:
                break
            
            if not data:
                print('Ta brekano')
                break
            
            if data.decode() == 'Aplicacao':
                client_socket.sendall(json.dumps(self.dispositivos).encode())
                self.verificar_conexao_ativa()

            if data.decode() == 'Bomba':
                client_socket.sendall(json.dumps(self.dispositivos).encode())
            else:
                if data.decode() != 'batman':
                    try:
                        client_socket.sendall(b'coringa')
                    except KeyError:
                            pass
            print("Dispositvos ",self.dispositivos)
        client_socket.close()


    
    
    def udp_server(self):
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.bind((self.address, self.udp_port))
        
        print(f"UDP Server {self.udp_port}")

        while True:
            
            data, addr = udp_server.recvfrom(1024)      #### RECEBE
            
            if data.decode() != 'batman':
                    try:
                        self.dispositivos[addr[0]][addr[1]] = data.decode()
                    except KeyError:
                            self.dispositivos[addr[0]] = {(addr[1]) : data.decode()}
            print(f"UDP {addr}: {data.decode()}")



 
    def verificar_conexao_ativa(self):
        udp_teste = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_teste.settimeout(5)
        try:
            for i in self.dispositivos:
                for j in self.dispositivos[i]:
                    udp_teste.sendto(b'ping',(i,j))    ##MANDA
                    try:
                        data , addr = udp_teste.recvfrom(1024)    #RECEBE
                        if not data:
                            self.dispositivos.get((i),{}).pop(j, None)
                            self.verifica_ips()

                    except TimeoutError:
                        print("Timeout cancela")
                        print(self.dispositivos)
                        self.dispositivos.get((i),{}).pop(j, None)
                        self.verifica_ips()
        except RuntimeError:
            print("resove")


            


    def verifica_ips(self):
        try:
            for i in self.dispositivos:
                if len(self.dispositivos[i]) == 0:
                    self.dispositivos.pop(i, None)
        except RuntimeError:
            pass


    def buton(self, dic):
        if dic:
            for i in self.dispositivos:
                for j in self.dispositivos[i]:
                    for l in dic:
                        if int(dic[l]) == j:
                            a = self.dispositivos[i][j]
                            print("\n\n",a, "\n\n\n\n")
                            aux = json.loads(a)
                            aux["Boton"] = 1
                            self.dispositivos[i][j] = json.dumps(aux)

                            print(self.dispositivos,"AQQuiiiiiiiiiiiii\n\n\n")
                    





            








ip = '192.168.1.6'  #Ip do servidor 

if __name__ == "__main__":
    broker = Broker(tcp_port=12345, udp_port=25565,ip=ip)
    broker.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Encerando...")
