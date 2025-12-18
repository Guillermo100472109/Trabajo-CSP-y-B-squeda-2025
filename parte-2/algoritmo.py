import math
from abierta import Abierta
from cerrada import Cerrada
from array import array

class AStar:
    def __init__(self, grafo):
        self.grafo = grafo
        self.nodos_expandidos = 0

        # Pre-calcular latitudes y longitudes en radianes
        n = len(grafo.lat)
        self.lat_rad = [math.radians(grafo.lat[i] * 0.000001) for i in range(n)]
        self.lon_rad = [math.radians(grafo.lon[i] * 0.000001) for i in range(n)]
        
        # Pre-calcular cosenos de latitudes 
        self.cos_lat = [math.cos(lat) for lat in self.lat_rad]

    def heuristica(self, nodo, meta):
        lat1_rad = self.lat_rad[nodo]
        lon1_rad = self.lon_rad[nodo]
        lat2_rad = self.lat_rad[meta]
        lon2_rad = self.lon_rad[meta]
        
        d_lat = lat2_rad - lat1_rad
        d_lon = lon2_rad - lon1_rad
        
        # Calcular sin una sola vez
        sin_dlat = math.sin(d_lat * 0.5)
        sin_dlon = math.sin(d_lon * 0.5)
        
        a = sin_dlat * sin_dlat + self.cos_lat[nodo] * self.cos_lat[meta] * sin_dlon * sin_dlon
        
        # Evitar clamp con max/min en una línea
        a = max(0.0, min(1.0, a))
        
        # atan2 con sqrt es más estable que asin
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return 6371000 * c 

    def resolver(self, start, goal, n, usar_heuristica=True):
        self.nodos_expandidos = 0
        
        abierta = Abierta()
        cerrada = Cerrada(n)
        
        # Usar Array para distancias en lugar de diccionario
        g_scores = array('i', [int('10000000')] * (n + 1))
        g_scores[start] = 0
        
        # 3. OPTIMIZACIÓN: Usar lista pre-asignada para padres
        # -1 indicará que no tiene padre (None)
        parents = [-1] * (n + 1)
        
        # Cálculo inicial
        h_start = self.heuristica(start, goal) if usar_heuristica else 0
        abierta.push(h_start, start) # f = g + h = 0 + h
        
        while not abierta.is_empty():
            # Extraer el mejor nodo (O(log n))
            f_actual, actual = abierta.pop()
            
            if cerrada.contains(actual):
                continue
            self.nodos_expandidos += 1
            cerrada.add(actual)
            
            # Verificar meta
            if actual == goal:
                return self.reconstruir_camino(parents, actual), g_scores[actual], self.nodos_expandidos
            
            # Expandir vecinos
            # Asumimos que get_neighbors devuelve [(vecino_id, peso), ...]
            vecinos = self.grafo.get_neighbors(actual)
            
            for vecino, peso in vecinos:
                
                # Si ya está cerrado, saltamos (mejora enorme de velocidad)
                if cerrada.contains(vecino):
                    continue
                
                nuevo_g = g_scores[actual] + peso
                
                # Si encontramos un camino mejor hacia el vecino
                if nuevo_g < g_scores[vecino]:
                    g_scores[vecino] = nuevo_g
                    parents[vecino] = actual
                    
                    if usar_heuristica:
                        h = self.heuristica(vecino, goal)
                        f = nuevo_g + h
                    else:
                        f = nuevo_g
                    
                    # Insertamos en el Heap (O(log n))
                    abierta.push(f, vecino)
                    
        return None, 0, self.nodos_expandidos

    def reconstruir_camino(self, parents, current):
        path = []
        # Mientras current no sea -1 (nuestro valor para None)
        while current != -1:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path