def print_decorated_matrix(board, size):
    border = "+---" * size + "+"
    print(border)
    for i in range(size):
        row_str = "|"
        for j in range(size):
            cell = board[(i * size) + j]
            display_char = " " if cell == "." else cell
            row_str += f" {display_char} |"
        print(row_str)
        print(border)
        
def print_solution_matrix(solution, size):
    if not solution:
        print("No se encontró ninguna solución.")
        return

    board = [solution[i] for i in range(size * size)]

    border = "+---" * size + "+"
    print(border)
    for i in range(size):
        row_str = "|"
        for j in range(size):
            cell = board[i * size + j]
            row_str += f" {cell} |"
        print(row_str)
        print(border)

def make_rows(n):
    filas = []
    for i in range(n):
        inicio = i * n
        fin = inicio + n
        filas.append(list(range(inicio, fin)))
    return filas

def make_cols(n):
    columnas = []
    for i in range(n):
        inicio = i
        fin = n * n
        salto = n
        
        columnas.append(list(range(inicio, fin, salto)))
    return columnas


def equal_colors(*args): # Restricciones horizontales y verticales
        b = 0
        n = 0
        for i in args:
            if i == "O":
                b += 1
            elif i == "X":
                n += 1
        return b == n

def two_equal_colors(*args): # No más de dos colores seguidos
    for i in range(len(args)-2):
        if args[i] == args[i+1] == args[i+2] :
            return False
    return True