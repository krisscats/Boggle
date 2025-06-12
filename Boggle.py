#NOTAS (para guiar y no perdernos)
'Uso de random y unas varas ahi'
'Existen 16 dados, cada uno con 6 caras.'
'Matriz de 4x4 generada aleatoriamente con 16 dados con letras especificas'
'tiempo limite 180 segundos'
import random

def leer_config(config):
    with open(config, 'r') as f: # ruta_config es el archivo de configuracion y aqui lo lee
        tiempo = int(f.readline().strip())  # Primera línea del tiempo
        dados = []
        for linea in f:
            if linea.strip().endswith('.txt'): # Verifica si la línea termina con '.txt'
                archivo_diccionario = linea.strip()  # Última línea "diccionario.txt"
                break # rompe el bucle si encuentra el archivo de diccionario
            caras = [cara.strip().upper() for cara in linea.strip().split(',')]
            dados.append(caras)
    return tiempo, dados, archivo_diccionario

def cargar_diccionario(ruta_diccionario):
    with open(ruta_diccionario, 'r', encoding='utf-8') as f:
        return {palabra.strip().upper() for palabra in f}

# Aquí se leen los datos de configuración y pues le hacems uso
tiempo, dados, nombre_archivo_diccionario = leer_config('config.txt')
diccionario = cargar_diccionario(nombre_archivo_diccionario)

def generar_tablero(dados): 
    random.shuffle(dados)  # Barajar dados usando random
    tablero = []
    for dado in dados[:16]:  #  16 dados (para 4x4)
        cara = random.choice(dado) #random.choice(dado) selecciona una cara aleatoria de cada dado
        if cara == 'Q':  # Si sale "Q", forzar "QU"
            cara = 'QU'
        tablero.append(cara) #aqui se agrega la cara seleccionada al tablero
    # Convertir a matriz 4x4 
    return [tablero[i*4:(i+1)*4] for i in range(4)]
tablero = generar_tablero(dados)
print("Tablero random:")
for fila in tablero:
    print(fila)