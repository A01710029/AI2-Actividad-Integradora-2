"""
Este programa contiene las funciones para resolver la Situación Problema 2.

Autores:
Paulina Almada Martínez - A01710029
Miguel Ángel Barrón Sánchez - A01710304	
Jesús Alejandro Cedillo Zertuche - A01705442

Fecha de Creación:
07/11/2024
"""

import copy

"""
Lee y regresa los contenidos de un archivo txt.

Parámetros:
archivo (string): el archivo del que se quiere extraer el contenido.

Valor de Retorno:
contenido del archivo (string)

Complejidad: O(n)
"""
def leer_archivo(archivo):
    with open(archivo, 'r') as file:
        return file.read()
    
"""
En base a los contenidos de un archivo, extrae los datos necesarios.

Parámetros:
archivo (string): el archivo del que se quiere extraer el contenido.

Valor de Retorno:
N (int): el número de colonias.
distancias (list): una matriz de distancias entre las colonias.
capacidades (list): una matriz de capacidades máximas de flujo entre las colonias.
ubicaciones_centrales (list): una lista de las ubicaciones de las centrales.
nueva_central (tuple): la ubicación de la nueva central.

Complejidad: O(n)
"""
def procesar_entrada(archivo):
    contenido = leer_archivo(archivo).strip().split("\n")
    
    # Asignar el número de colonias
    N = int(contenido[0])

    # Leer las distancias entre las colonias (matriz NxN)
    distancias = []
    for i in range(1, N + 1):
        distancias.append(list(map(int, contenido[i].split())))

    # Leer las capacidades máximas de flujo entre las colonias (matriz NxN)
    capacidades = []
    for i in range(N + 1, 2 * N + 1):
        capacidades.append(list(map(int, contenido[i].split())))

    # Leer las ubicaciones de las centrales
    ubicaciones_centrales = []
    for i in range(2 * N + 1, 2 * N + 1 + N):
        # Convertir las coordenadas de formato "(x, y)" a tupla (x, y)
        coords = contenido[i].strip("()").split(",")
        ubicaciones_centrales.append((int(coords[0]), int(coords[1])))
    
    # La ubicación en el plano de la nueva central
    nueva_central = tuple(map(int, contenido[2 * N + 1 + N].strip("()").split(",")))

    return N, distancias, capacidades, ubicaciones_centrales, nueva_central

"""
Algoritmo base de Floyd para encontrar las distancias más cortas entre
todos los pares de nodos en un grafo ponderado.

Parámetros:
grafo (list): una matriz de adyacencia que representa el grafo.

Valor de Retorno:
dist (list): una matriz de adyacencia con las distancias más cortas entre todos los pares de nodos.

Complejidad O(v^3): donde v es el número de nodos en el grafo.
"""

def floyd(grafo):
    n = len(grafo)
    dist = copy.deepcopy(grafo) # Copiar el grafo para crear la matriz de distancias

    # El que se cuenta como nodo intermedio
    for k in range(n):
        # Nodo de inicio
        for i in range(n):
            # Nodo final
            for j in range(n):
                # Si hay una forma de llegar de i a j pasando por k
                if dist[i][k] != 0 and dist[k][j] != 0:
                    # Calcula la distancia pasando por ese nodo intermedio
                    nueva_distancia = dist[i][k] + dist[k][j]
                    # Si no hay una distancia previa o la nueva distancia es menor se actualiza la nueva distancia
                    if dist[i][j] == 0 or nueva_distancia < dist[i][j]:
                        dist[i][j] = nueva_distancia
    return dist

"""
En base a lo que regresa el algoritmo de Floyd,
se guarda en una cadena de texto las distancias más cortas entre todas las colonias.

Parámetros:
distancias (list): una matriz de adyacencia que representa el grafo.

Valor de Retorno:
salida (string): una cadena de texto con las distancias más cortas entre todas las colonias.

Complejidad O(n^2): donde n es el número de nodos en el grafo.
"""
def floyd_parte_1(N, distancias):
    distancias_floyd = floyd(distancias)
    salida = "Punto 01: \n \n"
    for i in range(N):
        for j in range(N):
            if i != j:
                salida += (f"Km de Colonia {i + 1} a Colonia {j + 1}: {distancias_floyd[i][j]}\n")
        salida += "\n"
    return salida

"""
Procesa la entrada y guarda la salida en un archivo de texto.

Parámetros:
entrada (string): el archivo de entrada.
salida (string): el archivo de salida.

Valor de Retorno:
Ninguno
"""
def procesar_salida(entrada, salida):
    # Procesas la entrada y lo guardas en variables
    N, distancias, capacidades, ubicaciones_centrales, nueva_central = procesar_entrada(entrada)

    # Parte 1
    floyd_salida_1 = floyd_parte_1(N, distancias)

    # Guardar las salidas en un archivo de texto
    with open(salida, 'w') as f:
        f.write(floyd_salida_1)

# Prueba 01
procesar_salida("AI2_E01_Entrada_1.txt", "AI2_E01_Salida_1.txt")
procesar_salida("AI2_E01_Entrada_2.txt", "AI2_E01_Salida_2.txt")