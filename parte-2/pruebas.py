import time
import random
import sys
from grafo import Grafo
from algoritmo import AStar

def carga_optimizada(nombre_mapa):
    """
    Carga el grafo leyendo la cabecera 'p' del archivo .co para reservar
    memoria antes de intentar guardar nada.
    """
    grafo = Grafo()
    ruta_gr = f"{nombre_mapa}.gr"
    ruta_co = f"{nombre_mapa}.co"

    print(f"--- Cargando {nombre_mapa} ---")
    t0 = time.time()

    # 1. Cargar coordenadas y PRE-RESERVAR memoria
    print(f"Leyendo coordenadas ({ruta_co})...")
    try:
        with open(ruta_co, 'r') as f:
            for line in f:
                # --- CORRECCIÓN: Detectar tamaño en el .co ---
                if line.startswith('p'):
                    # Formato: p aux sp co <nodos>
                    parts = line.split()
                    num_nodos = int(parts[-1])
                    grafo.reservar_tamano(num_nodos)

                elif line.startswith('v'):
                    parts = line.split()
                    nid = int(parts[1])
                    # Recuerda: Grafo.set_coords espera enteros puros (lat, lon)
                    # En los ficheros DIMACS: parts[2]=Longitud, parts[3]=Latitud
                    grafo.set_coords(nid, int(parts[3]), int(parts[2]))
                    
    except FileNotFoundError:
        print(f"Error: No se encontró {ruta_co}")
        sys.exit(1)
    except IndexError:
        print("Error: El archivo .co intentó guardar un nodo sin haber reservado memoria (falta línea 'p').")
        sys.exit(1)

    # 2. Cargar Grafo (Estructura)
    print(f"Leyendo estructura del grafo ({ruta_gr})...")
    try:
        with open(ruta_gr, 'r') as f:
            for line in f:
                if line.startswith('p'):
                    # Intentamos reservar de nuevo por seguridad.
                    # Si grafo.py tiene la protección 'if self.num_nodos > 0', no pasará nada.
                    parts = line.split()
                    num_nodos = int(parts[2])
                    grafo.reservar_tamano(num_nodos)
                
                elif line.startswith('a'):
                    parts = line.split()
                    # Usamos la inserción rápida
                    grafo.add_edge_direct(int(parts[1]), int(parts[2]), int(parts[3]))
    except FileNotFoundError:
        print(f"Error: No se encontró {ruta_gr}")
        sys.exit(1)

    t1 = time.time()
    print(f"Carga completada en {t1-t0:.2f} segundos.")
    print(f"Datos: {grafo.get_num_vertices()} nodos, {grafo.get_num_arcos()} arcos.")
    return grafo

def ejecutar_bateria(grafo, casos):
    solver = AStar(grafo)
    
    print("\n--- Iniciando Batería de Tests ---")
    print(f"{'Caso':<10} {'Inicio -> Fin':<25} {'Coste':<10} {'Expandidos':<12} {'Tiempo (s)':<10}")
    print("-" * 70)

    tiempos = []

    for i, (start, goal) in enumerate(casos):
        t_start = time.time()
        camino, coste, expandidos = solver.resolver(start, goal)
        t_end = time.time()
        
        duracion = t_end - t_start
        tiempos.append(duracion)
        
        txt_caso = f"{start} -> {goal}"
        # Si no hay camino, coste es 0 o None
        coste_str = str(coste) if camino else "No path"
        print(f"Test {i+1:<5} {txt_caso:<25} {coste_str:<10} {expandidos:<12} {duracion:.4f}")

    if tiempos:
        promedio = sum(tiempos) / len(tiempos)
        print("-" * 70)
        print(f"Tiempo promedio por consulta: {promedio:.4f} s")

if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    mapa = "USA-road-d.USA"  # Cambia a "USA-road-d.USA" para la prueba real
    
    # 1. Cargar Grafo
    grafo_global = carga_optimizada(mapa)
    
    # 2. Definir casos (Asegúrate de que los IDs existan en el mapa elegido)
    # Nota: Los IDs de NY son distintos a los de USA completo.
    # Si usas NY, IDs seguros son 1..264346
    casos_prueba = [
        (1, 500),         
        (100, 2000),      
        (1, 10000),     
    ]
    
    # Generar algunos aleatorios
    max_id = grafo_global.get_num_vertices()
    random.seed(42) # Para reproducibilidad
    for _ in range(3):
        u = random.randint(1, max_id)
        v = random.randint(1, max_id)
        casos_prueba.append((u, v))

    # 3. Ejecutar
    ejecutar_bateria(grafo_global, casos_prueba)