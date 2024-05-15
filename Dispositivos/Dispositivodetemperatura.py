import server
import socket
import random
import time
import threading
import json


def escuta(sock):
    print('Uncia')
    while True:
        try:
            data , addr = sock.recvfrom(1024)
            if data == b'ping':
                sock.sendto("Poke".encode(), addr)
        except ConnectionResetError:
            print("Perdeu conexão")
 


def main():
    # Criar um socket ipv4 com protocolo udp
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    server_address = (server.ip(), 25565) #Servidor ip/porta

    a = threading.Thread(target=escuta,args=(sock_udp,))
    a.daemon = True

    msg = 40

    dispo = {"nome" : "Temperatura", "dado": f"{msg}°C"}
    thread = True
    while True:
        dispo["dado"] = f"{msg+ random.randint(-1,1)}°C"
        try:
            sock_udp.sendto(json.dumps(dispo).encode(), server_address) 
            if thread:
                a.start() 
                thread = False 
            


        except TimeoutError and OSError:
            print("Broker Desligado")

        time.sleep(1)



    
    
  


main()
