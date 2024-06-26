import server
import socket

import time
import threading
import json







def tcp_():
        server_address = (server.ip(), 12345)
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                sock_tcp.connect(server_address)
                threading.Thread(target=tcp_escuta,args=(sock_tcp,)).start()
                break
            except TimeoutError and ConnectionRefusedError and OSError:
                print("Conexão Com broker Falhou")



def tcp_escuta(sock_tcp):
    global addr
    while True:
        try:
            # Envie dados
            
            sock_tcp.sendall("Bomba".encode())

            # Receba uma resposta
            try:
                data = sock_tcp.recv(1024)
                dic = json.loads(data.decode())
            except TimeoutError and BrokenPipeError and json.decoder.JSONDecodeError:
                dic = {}
                print("Falha na comunicação com broker")
            for i in dic:
                if i == addr[0]:
                    for j in dic[i]:
                        if j == str(addr[1]):
                            aux = dic[i][j]
                            fec = json.loads(aux)
                            if fec["Boton"] == 1:
                                if fec["dado"] == "Desativado":
                                    dispo["dado"] = "Ativado"
                                else:
                                    dispo["dado"] = "Desativado"
                            
                        
            ##print(dispo)
            time.sleep(0.3)

        except ConnectionResetError:
            print("Conexão Com Broker Perdida")
            break

    tcp_()

            
    



def escuta(sock):
        while True:
            try:
                data , addr = sock.recvfrom(1024)
                if data == b'ping':
                    sock.sendto("Poke".encode(), addr)
        except ConnectionResetError:
            print("Perdeu conexão")


def udp_():
    # Criar um socket ipv4 com protocolo udp
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind(('192.168.1.6',0))

    
    server_address = (server.ip(), 25565) #Servidor ip/porta

    a = threading.Thread(target=escuta,args=(sock_udp,))
    a.daemon = True

    global addr, dispo

    dispo = {"nome" : "Bomba", "dado": "Desativado" , "Boton" : 0}
    thread = True
    while True:
        try:
            sock_udp.sendto(json.dumps(dispo).encode(), server_address) 
            addr = sock_udp.getsockname()
            if thread:
                a.start() 
                thread = False 
            


        except TimeoutError and OSError:
            print("Broker Desligado")

        time.sleep(3)


b = threading.Thread(target=tcp_)
b.daemon = True
print("Iniciando Conexão com Broker")
b.start()
udp_()
