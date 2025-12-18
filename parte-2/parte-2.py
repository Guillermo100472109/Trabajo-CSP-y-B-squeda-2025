import sys
import time
from grafo import Grafo
from algoritmo import AStar

def cargar_datos(nombre_mapa):
    grafo = Grafo()
    archivo_gr = f"{nombre_mapa}.gr"
    archivo_co = f"{nombre_mapa}.co"
    
    # 1. Cargar Coordenadas
    print(f"Cargando coordenadas ({archivo_co})...")
    try:
        with open(archivo_co, 'r') as f:
            for line in f:
                # DETECTAR TAMAÑO EN EL .CO
                if line.startswith('p'):
                    # Formato: p aux sp co <nodos>
                    parts = line.split()
                    num_nodos = int(parts[-1])
                    grafo.reservar_tamano(num_nodos)

                elif line.startswith('v'):
                    parts = line.split()
                    nid = int(parts[1])
                    lon = int(parts[2]) 
                    lat = int(parts[3])
                    grafo.set_coords(nid, lat, lon)
    except FileNotFoundError:
        print(f"Error: No se encontró {archivo_co}")
        sys.exit(1)
    except IndexError:
        print("Error: El archivo .co no tiene cabecera 'p' o los IDs superan el tamaño.")
        sys.exit(1)

    # Cargar Grafo
    print(f"Cargando grafo ({archivo_gr})...")
    try:
        with open(archivo_gr, 'r') as f:
            for line in f:
                if line.startswith('p'):
                    parts = line.split()
                    num_nodos = int(parts[2])
                    grafo.reservar_tamano(num_nodos)
                
                elif line.startswith('a'):
                    parts = line.split()
                    u = int(parts[1])
                    v = int(parts[2])
                    w = int(parts[3])
                    grafo.add_edge_direct(u, v, w)
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
        print("Uso: python3 parte-2.py <inicio> <fin> <mapa> <salida>")
        return

    origen = int(sys.argv[1])
    destino = int(sys.argv[2])
    nombre_mapa = sys.argv[3]
    fichero_salida = sys.argv[4]

    grafo = cargar_datos(nombre_mapa)

    solver = AStar(grafo)

    start_time = time.time()
    camino, coste, expandidos = solver.resolver(origen, destino, num_nodos=grafo.get_num_vertices(), usar_heuristica=True)
    end_time = time.time()
    
    tiempo_total = end_time - start_time
    nodos_seg = expandidos / tiempo_total if tiempo_total > 0 else 0

    # Imprimir estadísticas
    print(f"# vertices: {grafo.get_num_vertices()}")
    print(f"# arcos: {grafo.get_num_arcos()}")
    
    if camino:
        print(f"Solución óptima encontrada con coste {coste}")
        print(f"Tiempo de ejecución: {tiempo_total:.2f} segundos")
        print(f"# expansiones: {expandidos} ({nodos_seg:.2f} nodes/sec)")

        guardar_salida(camino, grafo, fichero_salida)
    else:
        print("No se encontró camino.")

if __name__ == "__main__":
    main()