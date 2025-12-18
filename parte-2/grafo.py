from array import array

class Grafo:
    def __init__(self):
        self.adj = []
        self.lat = array('i')
        self.lon = array('i')
        self.num_arcos = 0
        self.num_nodos = 0

    def reservar_tamano(self, num_nodos):
       
        if self.num_nodos > 0:
            return

        tamano_real = num_nodos + 1
        self.adj = [None] * tamano_real
        self.lat = array('i', [0] * tamano_real)
        self.lon = array('i', [0] * tamano_real)
        self.num_nodos = tamano_real

    def add_edge_direct(self, u, v, w):

        if self.adj[u] is None:
            self.adj[u] = array('I')
        self.adj[u].append(v)
        self.adj[u].append(w)
        self.num_arcos += 1

    def get_neighbors(self, u):
        if u >= len(self.adj) or self.adj[u] is None:
            return []
        data = self.adj[u]
        vecinos = []
        for i in range(0, len(data), 2):
            vecinos.append((data[i], data[i+1]))
        return vecinos

    def get_coords(self, u):
        if u < len(self.lat) and self.lat[u] != 0:
            return (self.lat[u], self.lon[u])
        return None
        
    def get_num_vertices(self):
        return self.num_nodos - 1
    
    def get_num_arcos(self):
        return self.num_arcos
    
    def set_coords(self, nid, lat, lon):
        self.lat[nid] = lat
        self.lon[nid] = lon