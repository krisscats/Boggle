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
# Definir la ruta al archivo de configuración
config_path = 'config.txt'  # Cambia esto por la ruta correcta si es necesario
# Leer configuración y obtener dados
tiempo, dados, archivo_diccionario = leer_config(config_path)
tablero = generar_tablero(dados)
print("Tablero random:")
for fila in tablero:
    print(fila)
