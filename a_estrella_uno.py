import os
import csv
import json
import math
from heapq import heappop, heappush

# Función para leer el archivo CSV y obtener las rutas
def leer_rutas(filepath):
    rutas = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            puntos = row[0].replace("LINESTRING (", "").replace(")", "").split(", ")
            ruta = [(float(p.split()[1]), float(p.split()[0])) for p in puntos]
            rutas.append(ruta)
    return rutas

# Implementación del algoritmo A*
def a_estrella(rutas):
    mejor_ruta = None
    mejor_distancia = float('inf')
    
    for ruta in rutas:
        if len(ruta) < 2:
            continue
        
        # Calcular la distancia total de la ruta
        distancia_total = sum(distancia(ruta[j], ruta[j + 1]) for j in range(len(ruta) - 1))
        
        # Si es la mejor hasta ahora, actualizar
        if distancia_total < mejor_distancia:
            mejor_distancia = distancia_total
            mejor_ruta = ruta
    
    return mejor_ruta, mejor_distancia

# Función para calcular la distancia euclidiana entre dos puntos
def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) * 111000  # Convertir a metros

# Función para guardar los resultados en un archivo JSON
def guardar_resultados(mejor_ruta, rutas, filepath):
    resultados = {"mejor_camino": [{"latitude": p[0], "longitude": p[1]} for p in mejor_ruta]}
    
    for i, ruta in enumerate(rutas):
        if ruta == mejor_ruta:
            continue  # Evitar duplicaciones de la mejor ruta
        if len(ruta) == 2:
            resultados[f"camino_{i + 1}"] = "distancia entre puntos"
        else:
            resultados[f"camino_{i + 1}"] = [{"latitude": p[0], "longitude": p[1]} for p in ruta]
    
    with open(filepath, 'w') as file:
        json.dump(resultados, file, indent=4)


diccionario_nombres_archivos_entrada = {
    1: "tics_rutas.csv",
    2:" secretaria.csv",
}

# Ruta del archivo CSV y del archivo JSON de salida
numero_archivo = 2

nombre_archivo = diccionario_nombres_archivos_entrada[numero_archivo]

csv_filepath = os.path.join(os.path.dirname(__file__), 'entradas/'+nombre_archivo)

json_filepath = os.path.join(os.path.dirname(__file__), 'salidas/'+nombre_archivo.replace('csv','.json'))

# Leer las rutas del archivo CSV
rutas = leer_rutas(csv_filepath)

# Encontrar el mejor camino usando el algoritmo A*
mejor_ruta, mejor_distancia = a_estrella(rutas)

# Guardar los resultados en un archivo JSON
guardar_resultados(mejor_ruta, rutas, json_filepath)

print(f"Mejor ruta encontrada {mejor_ruta} con una distancia de {mejor_distancia:.2f} metros")
