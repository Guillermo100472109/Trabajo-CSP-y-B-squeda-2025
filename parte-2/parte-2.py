import sys
#from .grafo import *
#from .abierta import *
#from .cerrada import *
#<from .algoritmo import *


#TODO Probar la lectura de los archivos .co y .gr
def main():
    #Lectura del .co con las coordenadas del nodo inicial y del nodo objetivo
    if len(sys.argv) != 5:
        print("Uso: python3 parte-2.py <vertice-1> <vertice-2> <nombre_mapa> <fichero_salida>")
        sys.exit(1)

    v1 = int(sys.argv[1])
    v2 = int(sys.argv[2])

    # nombre del mapa -> hay que usando este leer su .gr y su .co
    mapa = sys.argv[3] 
    coordenadas = open(mapa + ".co", "r")
    grafo = open(mapa + ".gr", "r")
    salida = sys.argv[4]
    print(f"Mapa: {mapa}, Vertice inicial: {v1}, Vertice objetivo: {v2}, Fichero salida: {salida}")

    # Lectura del fichero de entrada
    with coordenadas as c:
        n = v1 + 7
        linea = c.read()

    print(linea)


    #Lectura del .gr con las distancias entre dos nodos

if __name__ == "__main__":
    main()