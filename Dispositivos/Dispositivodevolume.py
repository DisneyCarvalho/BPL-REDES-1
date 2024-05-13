import server
import socket
import random
import time
import threading
import json


def escuta(sock):
    print('Uncia')
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

    msg = 6000000

    dispo = {"nome" : "Volume", "dado": msg}
    thread = True
    while True:
        dispo["dado"] += random.randint(-10,10)
        try:
            sock_udp.sendto(json.dumps(dispo).encode(), server_address) 
            if thread:
                a.start() 
                thread = False 
            


        except TimeoutError:
            print("Broker Desligado")

        time.sleep(1)



    
    
  


main()
