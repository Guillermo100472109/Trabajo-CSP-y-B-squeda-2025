import math
from abierta import Abierta
from cerrada import Cerrada

class AStar:
    def __init__(self, grafo):
        self.grafo = grafo
        self.nodos_expandidos = 0

    def heuristica(self, nodo, meta):
        c1 = self.grafo.get_coords(nodo)
        c2 = self.grafo.get_coords(meta)
        
        if not c1 or not c2:
            return 0
            
        lat1, lon1 = c1
        lat2, lon2 = c2
        
        R = 6371000  # Radio Tierra en metros
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(d_lat / 2)**2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(d_lon / 2)**2)
             
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = R * c

        return distancia * 10

    def resolver(self, start, goal, usar_heuristica=True):
        """
        Resuelve el problema. 
        Si usar_heuristica=True, ejecuta A* (Búsqueda Informada).
        Si usar_heuristica=False, ejecuta Dijkstra (Fuerza Bruta / Coste Uniforme).
        """
        self.nodos_expandidos = 0
        
        abierta = Abierta()
        cerrada = Cerrada()
        
        # g_score: coste real desde start
        g = {start: 0}
        # parents: para reconstruir camino
        parents = {start: None}
        
        # f inicial
        # Si es Dijkstra, h=0, por tanto f = g
        h_start = self.heuristica(start, goal) if usar_heuristica else 0
        abierta.push(h_start, start)
        
        coste_final = -1
        
        while not abierta.is_empty():
            f_actual, actual = abierta.pop()
            
            if cerrada.contains(actual):
                continue
            
            self.nodos_expandidos += 1
            cerrada.add(actual)
            
            if actual == goal:
                coste_final = g[actual]
                return self.reconstruir_camino(parents, actual), coste_final, self.nodos_expandidos
            
            vecinos = self.grafo.get_neighbors(actual)
            for vecino, peso in vecinos:
                if cerrada.contains(vecino):
                    continue
                
                nuevo_g = g[actual] + peso
                
                if vecino not in g or nuevo_g < g[vecino]:
                    g[vecino] = nuevo_g
                    parents[vecino] = actual
                    
                    # CÁLCULO DE F
                    if usar_heuristica:
                        h = self.heuristica(vecino, goal)
                        f = nuevo_g + h  # A* (f = g + h)
                    else:
                        f = nuevo_g      # Dijkstra (f = g)
                    
                    abierta.push(f, vecino)
                    
        return None, 0, self.nodos_expandidos

    def reconstruir_camino(self, parents, current):
        path = []
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path