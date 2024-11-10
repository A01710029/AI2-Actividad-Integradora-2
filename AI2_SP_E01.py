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
from collections import deque

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

    # Parte 2
    arbol_prim = prim(N, distancias)
    recorrido, costo_total = recorrido_preorden(N, arbol_prim, distancias)
    prim_salida_2 = prim_parte_2(recorrido, costo_total)

    # Parte 3
    origen = 0
    destino = N - 1
    flujo_max = edmonds_karp(capacidades, origen, destino)

    # Guardar las salidas en un archivo de texto
    with open(salida, 'w') as f:
        f.write(floyd_salida_1)
        f.write(prim_salida_2)
        f.write(flujo_max)

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

def prim(N, distancias):
    # Variables iniciales
    clave = [float('inf')] * N  # Para almacenar las claves de los vértices
    padre = [-1] * N  # Para almacenar los padres de los vértices
    visitado = [False] * N  # Para marcar los vértices visitados
    clave[0] = 0  # Comenzamos desde el vértice 0
    arbol = []  # Lista para almacenar el árbol (conjunto de aristas)

    for _ in range(N):
        # Encontramos el vértice con la clave más baja
        u = min_clave(N, clave, visitado)
        visitado[u] = True

        # Agregamos la arista al árbol si no es el vértice raíz
        if padre[u] != -1:
            arbol.append((padre[u], u))

        # Actualizamos las claves de los vértices adyacentes
        for v in range(N):
            if distancias[u][v] != 0 and not visitado[v] and distancias[u][v] < clave[v]:
                clave[v] = distancias[u][v]
                padre[v] = u

    return arbol

def min_clave(N, clave, visitado):
    # Encontramos el vértice con la clave más baja que no ha sido visitado
    min_valor = float('inf')
    min_indice = -1
    for i in range(N):
        if not visitado[i] and clave[i] < min_valor:
            min_valor = clave[i]
            min_indice = i
    return min_indice

def recorrido_preorden(N, arbol, distancias):
    # Construimos un grafo basado en el árbol de expansión mínima
    grafo_arbol = {i: [] for i in range(N)}
    for u, v in arbol:
        grafo_arbol[u].append(v)
        grafo_arbol[v].append(u)

    # Realizamos el recorrido en preorden
    visitado = [False] * N
    recorrido = []
    costo_total = 0

    def dfs(v):
        visitado[v] = True
        recorrido.append(v)
        for vecino in grafo_arbol[v]:
            if not visitado[vecino]:
                # Sumar el costo de la arista al costo total
                nonlocal costo_total
                costo_total += distancias[v][vecino]
                print(costo_total)
                dfs(vecino)

    # Comenzamos el recorrido desde el vértice 0
    dfs(0)
    # Añadimos el nodo inicial al final del recorrido para regresar al punto de partida
    recorrido.append(0)
    # Añadir el costo de la última arista para regresar al nodo inicial
    costo_total += distancias[recorrido[-2]][recorrido[-1]]
    
    return recorrido, costo_total

def prim_parte_2(recorrido, costo_total):
    recorrido_formateado = " -> ".join(str(nodo + 1) for nodo in recorrido)  
    result = f"Punto 02: \n \n"
    result += f"El recorrido: {recorrido_formateado}\n"
    result += f"El costo: {costo_total}\n"

    return result

"""
Implementa el algoritmo de Búsqueda en Anchura (BFS) para encontrar un camino en un grafo.

Parámetros:
camino (list): lista de nodos de los nodos visitados.
grafo (list): matriz de adyacencia que representa el grafo.
origen (int): nodo donde empieza la búsqueda.
destino (int): nodo al que se quiere llegar.

Valor de Retorno:
bool: true/false dependiendo de si existe un camino desde el origen hasta el destino con capacidad disponible.

Complejidad O(n + m): donde n es el número de nodos y m el número de aristas en el grafo.
"""
def bfs(camino, grafo, origen, destino):
    n = len(grafo)
    visitado = [False] * n
    visitado[origen] = True
    cola = deque([origen]) # Para manejar los nodos que se deben visitar

    # Mientras haya nodos que deben visitarse
    while cola:
        nodo = cola.popleft()
        
        # Recorrer vecinos del nodo
        for vecino, capacidad in enumerate(grafo[nodo]):
            # Si no se ha visitado y tiene capacidad
            if not visitado[vecino] and capacidad > 0:
                cola.append(vecino)
                visitado[vecino] = True
                camino[vecino] = nodo # Construir camino
                # Si se llega al destino, existe un camino 
                if vecino == destino:
                    return True
    return False

"""
Implementa el algoritmo de Edmonds-Karp para encontrar el flujo máximo en un grafo.

Parámetros:
grafo (list): matriz de adyacencia que representa el grafo.
origen (int): nodo donde se inicia a calcular el flujo máximo.
destino (int): nodo al cual se quiere llegar.

Valor de Retorno:
str: cadena de texto con el flujo máximo calculado.

Complejidad O(n * m^2): donde n es el número de nodos y m el número de aristas en el grafo.
"""
def edmonds_karp(grafo, origen, destino):
    n = len(grafo)
    flujo_maximo = 0
    grafo_residual = [fila[:] for fila in grafo] # Crear copia del grafo

    camino = [-1] * n

    # Hasta que se encuentre un camino
    while bfs(camino, grafo_residual, origen, destino):
        flujo_camino = float('Inf') # Para guardar flujo mínimo del camino definido
        nodo = destino
        
        # Calcular flujo mínimo del camino definido
        while nodo != origen:
            flujo_camino = min(flujo_camino, grafo_residual[camino[nodo]][nodo])
            nodo = camino[nodo]
        
        # Actualizar capacidades mientras se recorre el camino
        nodo = destino
        while nodo != origen:
            anterior = camino[nodo]
            grafo_residual[anterior][nodo] -= flujo_camino # Restar flujo al camino hacia adelante
            grafo_residual[nodo][anterior] += flujo_camino # Sumar flujo al camino hacia atrás
            nodo = camino[nodo]

        flujo_maximo += flujo_camino # Sumar flujo del camino para obtener total

    result = f"\nPunto 03: \n \n"
    result += f"Flujo maximo: {flujo_maximo}\n"

    return result

# Casos de Pruebas
procesar_salida("Entradas y Salidas/AI2_E01_Entrada_1.txt", "Entradas y Salidas/AI2_E01_Salida_1.txt")
procesar_salida("Entradas y Salidas/AI2_E01_Entrada_2.txt", "Entradas y Salidas/AI2_E01_Salida_2.txt")
procesar_salida("Entradas y Salidas/AI2_E01_Entrada_3.txt", "Entradas y Salidas/AI2_E01_Salida_3.txt")