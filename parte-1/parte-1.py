import sys
from constraint import *
from aux1 import *


def main():
    if len(sys.argv) != 3:
        print("Uso: python parte-1.py <fichero_entrada> <fichero_salida>")
        sys.exit(1)
    entrada = sys.argv[1]
    salida = sys.argv[2]

    tablero: list = []
    entrada = open(entrada, "r")

    # Lectura del fichero de entrada
    with entrada as e:
        n = int(e.readline().strip())
        for _ in range(n):
            linea = e.readline().strip()
            tablero.extend(linea)

    problem = Problem()

    # Creacion de las variables con python-constraint
    for position, cell_value in enumerate(tablero):
        if cell_value == ".":
            problem.addVariable(position, ["X","O"])
        elif cell_value == "X":
            problem.addVariable(position, ["X"])
        elif cell_value =="O":
            problem.addVariable(position, "O")

    # Añadir las restricciones al problema

    rows = make_rows(n)
    cols = make_cols(n)
    #print(cols)
    #print(rows)    


    for i in rows:
        problem.addConstraint(equal_colors, i)
        problem.addConstraint(two_equal_colors,i)
    for i in cols:
        problem.addConstraint(equal_colors, i)
        problem.addConstraint(two_equal_colors,i)


    print("Estado inicial del tablero:")
    print_decorated_matrix(tablero, n)

    soluciones = problem.getSolutions()
     
    print(f"{len(soluciones)} soluciones encontradas")

    original_stdout = sys.stdout
    with open(salida, 'w') as f:
        sys.stdout = f  # Redirigimos print al fichero
        
        print_decorated_matrix(tablero, n)
        print("") # Separador
        
        if len(soluciones) > 0:
            # Imprimimos la primera solución encontrada
            # Convertimos el diccionario de solución a lista/matriz para tu función de print
            solucion_dict = soluciones[0]
            solucion_lista = [solucion_dict[i] for i in range(n*n)]
            print_solution_matrix(solucion_lista, n)
            
        sys.stdout = original_stdout # Restauramos salida

if __name__ == "__main__":
    main()