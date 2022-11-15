import json
from threading import Thread
from server import Server


try:
    print("\nEsperando a que el cliente se conecte...")
    server = Server()
    print("\nSocket en funcionamiento.")
    
    thread = Thread(target=server.main())
    thread.start()
        
except KeyboardInterrupt:
    
    print("\n* * * * * * * * * * * * *\n")
    print("El programa ha sido interrumpido de forma repentina.")
    print("Cerrando conexión y liberando el puerto.\n")

except json.decoder.JSONDecodeError or ConnectionResetError:
    
    print("\n* * * * * * * * * * * * *\n")
    print("El cliente ha dejado de responder.")
    print("Cerrando conexión y liberando el puerto.\n")

except OSError:
    
    print("\nLa dirección a la que busca acceder ya está en uso.")
    print("Revise si el servidor ya está corriendo en otra terminal.\n")

finally:
    
    server.c.close()
