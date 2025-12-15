import sys
import time
from grafo import Grafo
from algoritmo import AStar

def cargar_datos(nombre_mapa):
    grafo = Grafo()
    archivo_gr = f"{nombre_mapa}.gr"
    archivo_co = f"{nombre_mapa}.co"
    
    # 1. Cargar Coordenadas (.co)
    try:
        with open(archivo_co, 'r') as f:
            for linea in f:
                if linea.startswith('v'):
                    partes = linea.split()
                    # Formato: v id lon lat (enteros * 10^6)
                    nid = int(partes[1])
                    lon = int(partes[2]) / 1000000.0
                    lat = int(partes[3]) / 1000000.0
                    grafo.set_coords(nid, lat, lon)
    except FileNotFoundError:
        print(f"Error: No se encontró {archivo_co}")
        sys.exit(1)

    # 2. Cargar Grafo (.gr)
    try:
        with open(archivo_gr, 'r') as f:
            for linea in f:
                if linea.startswith('a'):
                    partes = linea.split()
                    # Formato: a u v w
                    u = int(partes[1])
                    v = int(partes[2])
                    w = int(partes[3])
                    grafo.add_edge(u, v, w)
    except FileNotFoundError:
        print(f"Error: No se encontró {archivo_gr}")
        sys.exit(1)
        
    return grafo

def guardar_salida(camino, grafo, fichero_salida):
    if not camino:
        return
        
    salida_str = str(camino[0])
    coste_total = 0
    
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i+1]
        
        # Buscar coste de la arista u->v
        peso_arista = 0
        vecinos = grafo.get_neighbors(u)
        for vecino, peso in vecinos:
            if vecino == v:
                peso_arista = peso
                break
        
        salida_str += f" - ({peso_arista}) - {v}"
        
    try:
        with open(fichero_salida, 'w') as f:
            f.write(salida_str)
    except IOError:
        print("Error escribiendo fichero de salida")

def main():
    if len(sys.argv) != 5:
        print("Uso: python parte-2.py <inicio> <fin> <mapa> <salida>")
        return

    origen = int(sys.argv[1])
    destino = int(sys.argv[2])
    nombre_mapa = sys.argv[3]
    fichero_salida = sys.argv[4]

    # Cargar grafo
    grafo = cargar_datos(nombre_mapa)

    # Instanciar algoritmo
    solver = AStar(grafo)

    # Ejecutar y medir tiempo
    start_time = time.time()
    camino, coste, expandidos = solver.resolver(origen, destino)
    end_time = time.time()
    
    tiempo_total = end_time - start_time
    nodos_seg = expandidos / tiempo_total if tiempo_total > 0 else 0

    # Imprimir estadísticas por consola según formato [cite: 130-136]
    print(f"# vertices: {grafo.get_num_vertices()}")
    print(f"# arcos: {grafo.get_num_arcos()}")
    
    if camino:
        print(f"Solución óptima encontrada con coste {coste}")
        print(f"Tiempo de ejecución: {tiempo_total:.2f} segundos")
        print(f"# expansiones: {expandidos} ({nodos_seg:.2f} nodes/sec)")
        
        # Guardar fichero
        guardar_salida(camino, grafo, fichero_salida)
    else:
        print("No se encontró camino.")

if __name__ == "__main__":
    main()