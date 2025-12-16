=== PARTE 1 (CSP) ===
Ubicación: carpeta /parte-1

Ejecutar batería de pruebas automática:
$ sh pruebas.sh

Ejecución manual:
$ python3 parte-1.py <archivo_entrada> <archivo_salida>


=== PARTE 2 (Búsqueda) ===
Ubicación: carpeta /parte-2
Nota: Requiere los ficheros del mapa (.gr y .co) en el mismo directorio.

Ejecutar batería de pruebas comparativa (A* vs Dijkstra):
$ python3 pruebas.py

Ejecución manual para una ruta:
$ python3 parte-2.py <inicio> <fin> <mapa> <salida>
(Ejemplo: python3 parte-2.py 1 500 USA-road-d.NY salida.txt)