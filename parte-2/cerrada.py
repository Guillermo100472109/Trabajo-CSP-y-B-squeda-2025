# En la lista cerrada simplemente guardamos un conjunto de nodos ya expandidos.
class Cerrada:
    def __init__(self):
        self.elementos = set()
        
    def add(self, nodo):
        self.elementos.add(nodo)
        
    def contains(self, nodo):
        return nodo in self.elementos