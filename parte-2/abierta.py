class Abierta:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def push(self, f, nodo):
        self.heap.append((f, nodo))
        self._flotar(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
    
        min_nodo = self.heap[0]
        
        ultimo = self.heap.pop()
        
        if self.heap:
            self.heap[0] = ultimo
            self._hundir(0)
            
        return min_nodo

    #  Métodos Privados  

    def _flotar(self, indice):
        while indice > 0:
            padre_idx = (indice - 1) // 2
            
            if self.heap[indice][0] < self.heap[padre_idx][0]:
                self.heap[indice], self.heap[padre_idx] = self.heap[padre_idx], self.heap[indice]
                indice = padre_idx
            else:
                break

    def _hundir(self, indice):
        longitud = len(self.heap)
        
        while True:
            izq = 2 * indice + 1
            der = 2 * indice + 2
            menor = indice
            
            # ¿Es el hijo izquierdo menor que el nodo actual?
            if izq < longitud and self.heap[izq][0] < self.heap[menor][0]:
                menor = izq
                
            # ¿Es el hijo derecho menor que el más pequeño encontrado hasta ahora?
            if der < longitud and self.heap[der][0] < self.heap[menor][0]:
                menor = der
            
            # Si encontramos un hijo menor, intercambiamos y seguimos bajando
            if menor != indice:
                self.heap[indice], self.heap[menor] = self.heap[menor], self.heap[indice]
                indice = menor
            else:
                # Si el nodo es menor que sus hijos, ya está bien colocado.
                break