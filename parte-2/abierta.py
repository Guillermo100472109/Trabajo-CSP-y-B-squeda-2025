import heapq
# Usamos heapq para la lista abierta ya que es extremadamente eficiente
# en operaciones de inserción y extracción del mínimo.

class Abierta:
    def __init__(self):
        self.heap = []
    
    def push(self, f, nodo):
        heapq.heappush(self.heap, (f, nodo))
        
    def pop(self):
        return heapq.heappop(self.heap)
        
    def is_empty(self):
        return len(self.heap) == 0