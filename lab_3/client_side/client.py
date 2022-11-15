import socket


class Client:
    def __init__(self):
        self.s = socket.socket()
    
    def conectar_a_servidor(self):
        self.s.connect(("", 12345))
        
    def leer_vector(self, v):
        v_list = []
        while len(v)<1 and not(len(v_list)==1 and v_list[0]=="s"):
            v_list = (input("\nIngrese el vector a ordenar o \"s\" para salir: ")).split(",")
            for e in v_list:
                if e.strip().isnumeric():
                    v.append(int(e.strip()))
                else:
                    if not(len(v_list)==1 and v_list[0]=="s" 
                        or ((e.strip().isspace() or e.strip()=="")
                            and v_list.index(e)==len(v_list)-1
                            and len(v)>1)):
                        print("El vector ingresado no cumple con las "+
                            "instrucciones dadas:\nEl elemento \""+e.strip()+
                            "\" no puede añadirse al vector. \nRecuerde que "+
                            "solo puede contener números y debe separarlos "+
                            "por comas.")
                        v = []
                        break

    def escoger_algoritmo(self):
        # Preguntamos que algoritmo quiere escoger
        print("Escoja entre los algoritmos de ordenamiento:"+
              "\n1. MergeSort.\n2. HeapSort.\n3. QuickSort.")
        opc = (input("Ingrese su opción: ")).strip()
                
        while opc not in ("1", "2", "3"):
            print("Opción inválida. Intente de nuevo.")
            opc = (input("\nIngrese su opción: ")).strip()
            
        return opc