import time
import random
import sys
import os
from grafo import Grafo
from algoritmo import AStar

def carga_optimizada(nombre_mapa):
    grafo = Grafo()
    ruta_gr = f"{nombre_mapa}.gr"
    ruta_co = f"{nombre_mapa}.co"

    print(f"--- Cargando {nombre_mapa} ---")
    t0 = time.time()

    print(f"Leyendo coordenadas ({ruta_co})...")
    try:
        with open(ruta_co, 'r') as f:
            for line in f:
                if line.startswith('p'):
                    parts = line.split()
                    # p aux sp co <num_nodos>
                    num_nodos = int(parts[-1])
                    grafo.reservar_tamano(num_nodos)

                elif line.startswith('v'):
                    parts = line.split()
                    nid = int(parts[1])
                    grafo.set_coords(nid, int(parts[3]), int(parts[2]))
                    
    except FileNotFoundError:
        print(f"Error: No se encontró {ruta_co}")
        sys.exit(1)
    except IndexError:
        print("Error al leer coordenadas. Posible falta de cabecera 'p'.")
        sys.exit(1)

    # Cargar Grafo 
    print(f"Leyendo estructura del grafo ({ruta_gr})...")
    try:
        with open(ruta_gr, 'r') as f:
            for line in f:
                if line.startswith('p'):
                    parts = line.split()
                    num_nodos = int(parts[2])
                    grafo.reservar_tamano(num_nodos)
                
                elif line.startswith('a'):
                    parts = line.split()
                    grafo.add_edge_direct(int(parts[1]), int(parts[2]), int(parts[3]))
    except FileNotFoundError:
        print(f"Error: No se encontró {ruta_gr}")
        sys.exit(1)

    t1 = time.time()
    print(f"Carga completada en {t1-t0:.2f} s.")
    print(f"Grafo en memoria: {grafo.get_num_vertices()} nodos, {grafo.get_num_arcos()} arcos.")
    return grafo

def guardar_salida(camino, grafo, fichero_salida):
    if not camino:
        return
    salida_str = str(camino[0])
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i+1]
        peso_arista = "?"
        # Buscamos peso
        for vecino, peso in grafo.get_neighbors(u):
            if vecino == v:
                peso_arista = peso
                break
        salida_str += f" - ({peso_arista}) - {v}"
    try:
        with open(fichero_salida, 'w') as f:
            f.write(salida_str)
    except IOError:
        print(f"Error escribiendo {fichero_salida}")

def ejecutar_bateria(grafo, casos, n):
    solver = AStar(grafo)
    carpeta_salida = "resultados_tests"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    print("\n" + "="*105)
    print(f"{'Caso':<5} {'Inicio -> Fin':<22} | {'A* Exp.':<10} {'A* T(s)':<9} | {'Dijkstra Exp.':<14} {'Dijk. T(s)':<10} | {'Mejora':<8}")
    print("="*105)

    tiempos_astar = []

    for i, (start, goal) in enumerate(casos):
        txt_caso = f"{start} -> {goal}"

        # --- 1. Ejecutar A* (Heurística ACTIVADA) ---
        t0 = time.time()
        camino_a, coste, exp_a = solver.resolver(start, goal, n,  usar_heuristica=True)
        t_astar = time.time() - t0
        tiempos_astar.append(t_astar)

        # --- 2. Ejecutar Dijkstra (Heurística DESACTIVADA) ---
        t0 = time.time()
        _, _, exp_d = solver.resolver(start, goal,n, usar_heuristica=False)
        t_dijk = time.time() - t0

        # Calcular factor de mejora 
        if exp_a > 0:
            factor = t_dijk / t_astar
            mejora_str = f"{factor:.1f}x"
        else:
            mejora_str = "-"

        # Imprimir fila comparativa
        print(f"{i+1:<5} {txt_caso:<22} | {exp_a:<10} {t_astar:<9.4f} | {exp_d:<14} {t_dijk:<10.4f} | {mejora_str:<8}")
        
        # Guardar solución (solo una, son iguales)
        if camino_a:
            fname = os.path.join(carpeta_salida, f"solucion_caso_{i+1}.txt")
            guardar_salida(camino_a, grafo, fname)

    print("="*105)
    if tiempos_astar:
        print(f"Tiempo medio A*: {sum(tiempos_astar)/len(tiempos_astar):.4f} s")
    print(f"Ficheros de solución guardados en '{carpeta_salida}/'")

if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    mapa = "USA-road-d.NY"  # Cambia a .NY para pruebas rápidas
    
    grafo_global = carga_optimizada(mapa)
    
    casos_prueba = [
        (1, 500),         
        (100, 2000),      
        (1, 10000),     
    ]
    
    max_id = grafo_global.get_num_vertices()
    random.seed(42)
    for _ in range(3):
        u = random.randint(1, max_id)
        v = random.randint(1, max_id)
        casos_prueba.append((u, v))

    ejecutar_bateria(grafo_global, casos_prueba, max_id)