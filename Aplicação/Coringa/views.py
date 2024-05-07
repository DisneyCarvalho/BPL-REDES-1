from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
import socket
import threading
import json






class Aplication(APIView):

    def get(self, request, *args, **kwargs):
        return render(request, "test.html")
    


class boton(APIView):
    def post(self, request):
        obj = json.loads(request.body)
        
        print(obj)
        addr = ('192.168.1.6',12345)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(addr)

        try:
            # Envie dados
            
            sock.sendall(json.dumps(obj).encode())

            # Receba uma resposta
            data = sock.recv(1024)
            print('Recebido:', data.decode())

        finally:
            # Limpeza de recursos
            sock.close()


        return render(request, "test.html")
    




    

                


def get_data(request):
    broker_address = ('192.168.1.6', 12345)
    dispositivos = {}

    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.connect(broker_address)
        print("Mensagem enviada: Aplicacao")
        servidor.sendall("Aplicacao".encode())
        dispos = servidor.recv(1024).decode()
        print("Resposta recebida:", json.loads((dispos)))
        dispositivos = {"dispositivos": dispos}
    except ConnectionRefusedError:
        print("Broker Desligado")
    except OSError:
        print("Não foi possível enviar a mensagem")
    finally:
        servidor.close()

    return JsonResponse(dispositivos)



                


    
    


    
    

'''class get_data(View):
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.dispo = 1
        thread_estado = threading.Event()'''
        
        
    

    

    





        
        