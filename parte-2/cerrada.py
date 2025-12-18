# En la lista cerrada simplemente guardamos un conjunto de nodos ya expandidos.
#from array import array

class Cerrada:
    def __init__(self, n):
        self.elementos = [False] * n
        
    def add(self, nodo):
        self.elementos[nodo-1] = True
        
    def contains(self, nodo=int):
        return self.elementos[nodo-1]