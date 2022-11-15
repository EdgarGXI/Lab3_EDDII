import json
from client import Client


try:
    client = Client()
    client.conectar_a_servidor()
    
    while True:
        
        # Lee el vector y valida que este compuesto únicamente por números
        v = []
        client.leer_vector(v)
        
        if len(v)<1:
            
            # Si desea cerrar el programa
            data = json.dumps({"a": 1, "b": "5"})
            client.s.send(data.encode())
            break
        
        else:
            opc = client.escoger_algoritmo()
            print("\nArray original:", v)

            if opc != "3":
                # Si el algoritmo no tiene pivote
                
                # Codificamos el vector y una variable para indicarle al server 
                # lo que hay que hacer
                data = json.dumps({"a": v, "b": opc})
                
                # Mandamos la data codificada al server
                client.s.send(data.encode())
                
                # Recibimos una respuesta del server (esta es para el ping)
                rcvdData = client.s.recv(1024)
                rcvdData = json.loads(rcvdData.decode())
                
                # Se responde al server para que continúe
                data = json.dumps(rcvdData)
                client.s.send(data.encode())
                
                if opc == "1":
                    # Ejecutando MergeSort
                    print("\n* Ejecutando MergeSort *\n")
                    
                    print("Progreso de ordenamiento del array:")
                    while rcvdData.get("Flag") == "Bandera":
                        
                        # Recibimos respuestas del server
                        rcvdData = client.s.recv(1024)
                        rcvdData = json.loads(rcvdData.decode())
                        
                        # Si el server acaba el ordenamiento, 
                        # manda un ping para romper el ciclo
                        if rcvdData.get("Flag") != "Bandera":
                            break
                        else:
                            # Se imprime lo que nos manda el server
                            if (rcvdData.get("Side") != "Merge" 
                                and rcvdData.get("Side") != None):
                                print("Lado", rcvdData.get("Side"), 
                                    ":", rcvdData.get("arr"))
                            else:
                                print("Juntados:", rcvdData.get("arr"))
                                print("\nProgreso de ordenamiento del array:")
                            # Responde al server para que continúe
                            data = json.dumps(rcvdData)
                            client.s.send(data.encode())
                    print("Terminado de ordenar.")
                            
                elif opc == "2":
                    # Ejecutando HeapSort
                    print("\n* Ejecutando HeapSort *\n")
                    
                    while rcvdData.get("Flag") == "Bandera":
                        
                        # Recibimos respuestas del server
                        rcvdData = client.s.recv(1024)
                        rcvdData = json.loads(rcvdData.decode())
                        
                        # Si el server acaba el ordenamiento, 
                        # manda un ping para romper el ciclo
                        if rcvdData.get("Flag") != "Bandera":
                            break
                        else:
                            # Se imprime lo que nos manda el server
                            print("Como va quedando el array:", rcvdData.get("arr"))
                            # Responde al server para que continúe
                            data = json.dumps(rcvdData)
                            client.s.send(data.encode())
                
            else:
                # Ejecutando QuickSort
                
                pivote = (input("Seleccione su pivote (1/Izquierda o 2/Derecha): ")).strip()
                while pivote not in("1", "2"):
                    print("La opción ingresada es inválida. Intente de nuevo.")
                    pivote = (input("\nSeleccione su pivote (1/Izquierda o 2/Derecha): ")).strip()
                    
                print("\n* Ejecutando QuickSort *\n")
                
                if pivote == "1":
                    # Codificamos el vector y una variable para indicarle al server 
                    # lo que hay que hacer
                    data = json.dumps({"a": v, "b": "3"})
                    # Mandamos la data codificada al server
                    client.s.send(data.encode())
                    
                if pivote == "2":
                    # Codificamos el vector y una variable para indicarle al server 
                    # lo que hay que hacer
                    data = json.dumps({"a": v, "b": "4"})
                    # Mandamos la data codificada al server
                    client.s.send(data.encode())
                
                # Recibimos una respuesta del server (esta es para el ping)
                rcvdData = client.s.recv(1024)
                rcvdData = json.loads(rcvdData.decode())
                
                # Se responde al server para que continúe
                data = json.dumps(rcvdData)
                client.s.send(data.encode())
                    
                while rcvdData.get("Flag") == "Bandera":
                        
                    # Recibimos respuestas del server
                    rcvdData = client.s.recv(1024)
                    rcvdData = json.loads(rcvdData.decode())
                        
                    # Si el server acaba el ordenamiento, 
                    # manda un ping para romper el ciclo
                    if rcvdData.get("Flag") != "Bandera":
                        break
                    else:
                        # Se imprime lo que nos manda el server
                        print("Como va quedando el array:", rcvdData.get("arr"))
                        # Responde al server para que continúe
                        data = json.dumps(rcvdData)
                        client.s.send(data.encode())

            # Se imprime el resultado final
            print("\nTiempo de ejecución:", rcvdData.get("Flag"), "segundos")
            print("Resultado final:", rcvdData.get("arr"), "\n")    

    print("\nEl programa ha sido interrumpido.")
    print("Cerrando conexión y liberando el puerto.\n") 
    
except KeyboardInterrupt:
    # Para cerrar todo por si acaso
    print("\n* * * * * * * * * * * * *\n")
    print("El programa ha sido interrumpido de forma repentina.")
    print("Cerrando conexión y liberando el puerto.\n")

except ConnectionRefusedError:
    
    print("\nLa conexión ha sido negada. Revise si el servidor está corriendo.\n")

except json.decoder.JSONDecodeError or ConnectionResetError:
    
    print("\n* * * * * * * * * * * * *\n")
    print("El servidor ha dejado de responder")
    print("Cerrando conexión y liberando el puerto.\n")

finally:
    
    client.s.close()