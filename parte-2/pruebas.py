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

    # Cargar coordenadas y PRE-RESERVAR memoria
    print(f"Leyendo coordenadas ({ruta_co})...")
    try:
        with open(ruta_co, 'r') as f:
            for line in f:
                if line.startswith('p'):
                    parts = line.split()
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
        print("Error: El archivo .co intentó guardar sin reservar memoria.")
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
    print(f"Carga completada en {t1-t0:.2f} segundos.")
    print(f"Datos: {grafo.get_num_vertices()} nodos, {grafo.get_num_arcos()} arcos.")
    return grafo

# --- FUNCIÓN PARA GUARDAR FICHERO  ---
def guardar_salida(camino, grafo, fichero_salida):
    if not camino:
        return
        
    # Construimos el string con el formato requerido
    salida_str = str(camino[0])
    
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i+1]
        
        # Buscamos el peso de la arista u -> v
        # Como usamos el Grafo optimizado, iteramos sobre el generador de vecinos
        peso_arista = "?"
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

# --- BATERÍA DE PRUEBAS ---
def ejecutar_bateria(grafo, casos):
    solver = AStar(grafo)
    
    # Crear carpeta para resultados si no existe
    carpeta_salida = "resultados_tests"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    print("\n--- Iniciando Batería de Tests ---")
    print(f"{'Caso':<5} {'Inicio -> Fin':<25} {'Coste':<10} {'Exp.':<8} {'T(s)':<8} {'Fichero'}")
    print("-" * 80)

    tiempos = []

    for i, (start, goal) in enumerate(casos):
        t_start = time.time()
        camino, coste, expandidos = solver.resolver(start, goal)
        t_end = time.time()
        
        duracion = t_end - t_start
        tiempos.append(duracion)
        
        coste_str = str(coste) if camino else "No path"
        fichero_nombre = ""
        
        # Si hay camino, generamos el archivo
        if camino:
            fichero_nombre = f"solucion_caso_{i+1}.txt"
            ruta_completa = os.path.join(carpeta_salida, fichero_nombre)
            guardar_salida(camino, grafo, ruta_completa)
            fichero_nombre = f"Saved: {fichero_nombre}" # Para mostrar en tabla
        
        txt_caso = f"{start} -> {goal}"
        print(f"{i+1:<5} {txt_caso:<25} {coste_str:<10} {expandidos:<8} {duracion:.4f}   {fichero_nombre}")

    if tiempos:
        promedio = sum(tiempos) / len(tiempos)
        print("-" * 80)
        print(f"Tiempo promedio por consulta: {promedio:.4f} s")
        print(f"Los ficheros de solución están en la carpeta '{carpeta_salida}'")

if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    mapa = "USA-road-d.USA" # Cambiar por la que se quiera probar
    
    # 1. Cargar Grafo
    grafo_global = carga_optimizada(mapa)
    
    # 2. Definir casos
    casos_prueba = [
        (1, 500),         
        (100, 2000),      
        (1, 10000),     
    ]
    
    # Añadir aleatorios
    max_id = grafo_global.get_num_vertices()
    random.seed(42)
    for _ in range(3):
        u = random.randint(1, max_id)
        v = random.randint(1, max_id)
        casos_prueba.append((u, v))

    # 3. Ejecutar
    ejecutar_bateria(grafo_global, casos_prueba)