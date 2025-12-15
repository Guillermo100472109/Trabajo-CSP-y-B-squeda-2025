# Esta clase guarda los nodos con una lista de adyacencia y las coordenadas de cada nodo 
# en un diccionario. Se lee y se agrega la información del grafo desde el fichero .gr
class Grafo:
    def __init__(self):
        self.adj = {}
        self.coords = {}
        self.num_arcos = 0

    def add_edge(self, u, v, w):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, w))
        self.num_arcos += 1

    def set_coords(self, node_id, lat, lon):
        self.coords[node_id] = (lat, lon)

    def get_neighbors(self, u):
        return self.adj.get(u, [])

    def get_coords(self, u):
        return self.coords.get(u)
    
    def get_num_vertices(self):
        return len(self.coords)

    def get_num_arcos(self):
        return self.num_arcos