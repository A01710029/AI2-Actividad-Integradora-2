"""
Este programa contiene las funciones para resolver la Situación Problema 2.

Autores:
Paulina Almada Martínez - A01710029
Miguel Ángel Barrón Sánchez - A01710304	
Jesús Alejandro Cedillo Zertuche - A01705442

Fecha de Creación:
07/11/2024
"""

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
    
N, distancias, capacidades, ubicaciones_centrales, nueva_central = procesar_entrada("AI2_E01_Entrada_Y.txt")

print(f"N: {N}")
print(f"Distancias: {distancias}")
print(f"Capacidades: {capacidades}")
print(f"Ubicaciones Centrales: {ubicaciones_centrales}")
print(f"Nueva Central: {nueva_central}")