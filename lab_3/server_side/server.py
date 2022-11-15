import socket
import json
import time

class Server:
    def __init__(self):
        # Nos conectamos al cliente
        s = socket.socket()
        s.bind(("", 12345))
        s.listen(5)
        self.c = s.accept()[0]

    def merge(self, left, right):
        if not len(left) or not len(right):
            return left or right

        result = []
        i, j = 0, 0
        while (len(result) < len(left) + len(right)):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            if i == len(left) or j == len(right):
                result.extend(left[i:] or right[j:])
                break

        # Envía avance
        sendData = json.dumps(
            {"arr":  left, "Flag":  "Bandera", "Side":  "Izquierdo"})
        self.c.send(sendData.encode())

        # Espera respuesta para continuar
        rcvdData = self.c.recv(1024)
        rcvdData = json.loads(rcvdData.decode())

        # Envía avance
        sendData = json.dumps(
            {"arr":  right, "Flag":  "Bandera", "Side":  "Derecho"})
        self.c.send(sendData.encode())

        # Espera respuesta para continuar
        rcvdData = self.c. recv(1024)
        rcvdData = json.loads(rcvdData.decode())

        # Envía avance
        sendData = json.dumps(
            {"arr":  result, "Flag":  "Bandera", "Side":  "Merge"})
        self.c.send(sendData.encode())

        # Espera respuesta para continuar
        rcvdData = self.c. recv(1024)
        rcvdData = json.loads(rcvdData.decode())

        return result

    def mergesort(self, list):
        if len(list) < 2:
            return list

        middle = int(len(list)/2)
        left = self.mergesort(list[:middle])
        right = self.mergesort(list[middle:])
        r = self.merge(left, right)

        return r

    def heapify(self, arr, n, i):
        # Find largest among root and children
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        
        if l < n and arr[i] < arr[l]:
            largest = l
        
        if r < n and arr[largest] < arr[r]:
            largest = r
        
        # If root is not largest, swap with largest and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest)

    def heapsort(self, arr):
        # Envía avance
        sendData = json.dumps({"arr":  arr, "Flag":  "Bandera"})
        self.c.send(sendData.encode())

        # Espera respuesta para continuar
        rcvdData = self.c.recv(1024)
        rcvdData = json.loads(rcvdData.decode())

        n = len(arr)
        # Build max heap
        for i in range(n//2, -1, -1):
                self.heapify(arr, n, i)

        for i in range(n-1, 0, -1):
            # Swap
            sendData = json.dumps({"arr":  arr, "Flag":  "Bandera"})
            self.c.send(sendData.encode())

            # Espera respuesta para continuar
            rcvdData = self.c.recv(1024)
            rcvdData = json.loads(rcvdData.decode())
            arr[i], arr[0] = arr[0], arr[i]
            sendData = json.dumps({"arr":  arr, "Flag":  "Bandera"})
            self.c.send(sendData.encode())

            # Espera respuesta para continuar
            rcvdData = self.c.recv(1024)
            rcvdData = json.loads(rcvdData.decode())
            # Heapify root element
            self.heapify(arr, i, 0)
            sendData = json.dumps({"arr":  arr, "Flag":  "Bandera"})
            self.c.send(sendData.encode())

            # Espera respuesta para continuar
            rcvdData = self.c.recv(1024)
            rcvdData = json.loads(rcvdData.decode())
        # Envía avance
        sendData = json.dumps({"arr":  arr, "Flag":  "Bandera"})
        self.c.send(sendData.encode())

        # Espera respuesta para continuar
        rcvdData = self.c.recv(1024)
        rcvdData = json.loads(rcvdData.decode())
        return arr

    def partition_right(self, array, low, high):
        # choose the rightmost element as pivot
        pivot = array[high]

        # pointer for greater element
        i = low - 1

        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            # <= ascending | >= descending
            if array[j] <= pivot:
                # if element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
                # swapping element at i with element at j
                array[i], array[j] = array[j], array[i]

                # swap the pivot element with the greater element specified by i
        array[i+1], array[high] = array[high], array[i+1]

        # return the position from where partition is done
        return (i+1)

    def partition_left(self, array, low, high):
        # choose the rightmost element as pivot
        pivot = array[low]

        # pointer for smaller element
        i = low + 1

        # traverse through all elements
        # compare each element with pivot
        for j in range(low+1, high+1):
            # <= ascending | >= descending
            if array[j] < pivot:
                # if element smaller than pivot is found
                # swap it with the greater element pointed by i

                # swapping element at i with element at j
                array[i], array[j] = array[j], array[i]

                i += 1

                # swap the pivot element with the greater element specified by i
        #array[i+1], array[high] = array[high], array[i+1]
        array[low], array[i-1] = array[i-1], array[low]

        # return the position from where partition is done
        return (i-1)

    def quicksort(self, array, low, high, pivot):
        if low < high:
            # find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            if pivot == "1":
                pi = self.partition_left(array, low, high)
            else:
                pi = self.partition_right(array, low, high)

            # Envía avance
            sendData = json.dumps({"arr":  array, "Flag":  "Bandera"})
            self.c.send(sendData.encode())

            # Espera respuesta para continuar
            rcvdData = self.c.recv(1024)
            rcvdData = json.loads(rcvdData.decode())

            # recursive call on the left of pivot
            self.quicksort(array, low, pi-1, pivot)

            # recursive call on the right of pivot
            self.quicksort(array, pi+1, high, pivot)

        return array

    def main(self):
        while True:

            # Leemos los datos que nos mande el cliente
            rcvdData = self.c.recv(1024)

            # Decodificamos lo que nos mandó el cliente
            rcvdData = json.loads(rcvdData.decode())

            # Obtenemos el vector que nos mando el cliente y la opción que escogió
            v = rcvdData.get("a")
            b = rcvdData.get("b")

            if b != "5":
                # Mandamos un ping al cliente para que se mantenga a la espera del resultado
                sendData = json.dumps({"arr": 1, "Flag": "Bandera"})
                self.c.send(sendData.encode())

                # Espera respuesta del cliente para proseguir
                rcvdData = self.c.recv(1024)
                rcvdData = json.loads(rcvdData.decode())

                tic = time.perf_counter()
                # Aplicamos el algoritmo que pidió el cliente
                if b == "1":
                    v = self.mergesort(v)
                if b == "2":
                    v = self.heapsort(v)
                if b == "3":    # quicksort con pivote a la izquierda
                    v = self.quicksort(v, 0, len(v)-1, "1")
                if b == "4":    # quicksort con pivote a la derecha
                    v = self.quicksort(v, 0, len(v)-1, "2")
                toc = time.perf_counter()
                
                # Enviamos resultado al cliente 
                sendData = json.dumps({"arr": v, "Flag": f"{toc - tic:0.4f}"})
                self.c.send(sendData.encode())

            else:
                # Si el cliente quiere salir del programa
                print("\nEl programa ha sido interrumpido.")
                print("Cerrando conexión y liberando el puerto.\n")
                break
