import random
import time
import pickle

# ========= CLASES Y UTILIDADES PARA TRIE =========

class TrieNode:
    def __init__(self, char=''):
        self.char = char
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word.strip():
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_end_of_word = True

    def from_nested_list(self, nested, parent=None):
        char, children_list, is_end = nested
        node = TrieNode(char)
        node.is_end_of_word = is_end
        for child_nested in children_list:
            child_node = self.from_nested_list(child_nested, node)
            node.children[child_node.char] = child_node
        return node

    def load_from_nested_list_file(self, filename):
        with open(filename, 'rb') as f:
            nested = pickle.load(f)
        self.root = self.from_nested_list(nested)

# ========= JUGADOR PERFECTO =========

def qs(L):
    if L == []:
        return []
    menores = []
    mayores = []
    rata = L[0]  # Elegimos el primer elemento como pivote ("rata")
    for i in range(1, len(L)):
        if L[i] < rata:
            menores.append(L[i])
        else:
            mayores.append(L[i])
    return qs(menores) + [rata] + qs(mayores)


# Busca un hijo con una letra específica en un nodo del Trie
# El nodo tiene la forma: [letra, lista_de_hijos, es_fin_de_palabra]
def buscar_hijo(letra, nodo):
    for hijo in nodo[1]:
        if hijo[0] == letra:
            return hijo
    return None  # No se encontró la letra entre los hijos


# Búsqueda en profundidad sobre el tablero para formar palabras usando el Trie
def dfs(tablero, fila, col, nodo, palabra, visitadas, encontradas):
    filas, cols = len(tablero), len(tablero[0])

    # Verifica si estamos dentro del tablero y no hemos visitado ya esta celda
    if fila < 0 or fila >= filas or col < 0 or col >= cols: #Cimpara fila y columnas actuales con los límites del tablero 
        return #si nos pasamos
    if (fila, col) in visitadas: #si ya está visitada la celda para la palabra buscada
        return

    # Extrae las letras de la celda actual, puede ser "Q", que se trata como "QU"
    letras = tablero[fila][col]
    actual = nodo
    palabra_temp = palabra

    # Avanza por cada letra de la celda en el Trie
    for letra in letras:
        siguiente = buscar_hijo(letra, actual)
        if siguiente is None:
            return  # Si no existe ese camino, cortamos
        actual = siguiente
        palabra_temp += letra

    # Si llegamos a una palabra válida (mínimo 3 letras y fin de palabra), la agregamos si no estaba
    if actual[2] and len(palabra_temp) >= 3 and palabra_temp not in encontradas:
        encontradas.append(palabra_temp)

    # Continuamos buscando en todas las celdas vecinas (8 direcciones)
    visitadas.append((fila, col))
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr != 0 or dc != 0:
                dfs(tablero, fila + dr, col + dc, actual, palabra_temp, visitadas, encontradas)
    visitadas.pop()  # Retrocede: desmarca la celda como visitada


# Función principal del jugador perfecto: explora todo el tablero y devuelve todas las palabras válidas
def jugadorPerf(tablero, trie_root):
    filas, cols = len(tablero), len(tablero[0])
    encontradas = []

    # Empieza una búsqueda DFS desde cada celda del tablero
    for fila in range(filas):
        for col in range(cols):
            dfs(tablero, fila, col, trie_root, '', [], encontradas) #oarametros del DFS: tablero, fila, columna, nodo, palabra actual, celdas visitadas, palabras encontradas

    return qs(encontradas)  # Ordena las palabras encontradas alfabéticamente con quicksort, es opcional pero se ve más lindo :p

def calcular_puntaje(palabra):
    longitud = len(palabra)
    if longitud < 3:
        return 0
    elif longitud <= 4:
        return 1
    elif longitud == 5:
        return 2
    elif longitud == 6:
        return 3
    elif longitud == 7:
        return 5
    else:
        return 11

# ========= FUNCIONES PRINCIPALES =========

def jugar(tablero, diccionario, tiempo_limite):
    palabras_usadas = []
    puntaje_total = 0
    start_time = time.time()

    print(f"\n¡Tenés {tiempo_limite} segundos! Ingresá palabras (ENTER vacío para terminar):")
    while True:
        tiempo_restante = int(tiempo_limite - (time.time() - start_time))
        if tiempo_restante <= 0:
            print("\n¡Se acabó el tiempo!")
            break

        print(f"\nTiempo restante: {tiempo_restante}s")
        entrada = input("> ").strip().upper()

        if entrada == "":
            print("\nTerminaste la partida manualmente.")
            break

        if entrada in palabras_usadas:
            print("Ya usaste esa palabra.")
        elif not buscar_en_trie(diccionario, entrada):
            print("No está en el diccionario.")
        elif not esta_en_tablero(tablero, entrada):
            print("No se puede formar en el tablero.")
        else:
            palabras_usadas.append(entrada)
            puntos = calcular_puntaje(entrada)
            puntaje_total += puntos
            print(f"Válida ({puntos} puntos)")

    print(f"\nPuntaje final: {puntaje_total} puntos")

def buscar_en_trie(nodo, palabra):
    actual = nodo
    for letra in palabra:
        hijo = buscar_hijo(letra, actual)
        if hijo is None:
            return False
        actual = hijo
    return actual[2]  # es end de palabra

def esta_en_tablero(tablero, palabra):
    filas, columnas = len(tablero), len(tablero[0])
    palabra = palabra.upper()

    def backtrack(fila, col, palabra_restante, visitadas):
        if not palabra_restante:
            return True
        if (fila < 0 or fila >= filas or col < 0 or col >= columnas):
            return False
        if (fila, col) in visitadas:
            return False

        celda = tablero[fila][col]
        if not palabra_restante.startswith(celda):
            return False

        visitadas.add((fila, col))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    if backtrack(fila + dr, col + dc, palabra_restante[len(celda):], visitadas):
                        return True
        visitadas.remove((fila, col))
        return False

    for f in range(filas):
        for c in range(columnas):
            if backtrack(f, c, palabra, set()):
                return True
    return False

def leer_config(config):
    with open(config, 'r') as f:
        tiempo = int(f.readline().strip())
        dados = []
        for linea in f:
            if linea.strip().endswith('.txt'):
                archivo_diccionario = linea.strip()
                break
            caras = [cara.strip().upper() for cara in linea.strip().split(',')]
            dados.append(caras)
    return tiempo, dados, archivo_diccionario

def generar_tablero(dados):
    random.shuffle(dados)
    tablero = []
    for dado in dados[:16]:
        cara = random.choice(dado)
        if cara == 'Q':
            cara = 'QU'
        tablero.append(cara)
    return [tablero[i*4:(i+1)*4] for i in range(4)]

# ========= PROGRAMA PRINCIPAL =========

if __name__ == "__main__":
    tiempo, dados, _ = leer_config("C:/Users/oquai/Downloads/Boggle-main/Boggle-main/config.txt")
    nombre_diccionario = "C:/Users/oquai/Downloads/Boggle-main/Boggle-main/diccionario.txt"

    # Cargar el Trie sin clases
    with open("C:/Users/oquai/Downloads/Boggle-main/Boggle-main/trie_nested.pkl", "rb") as f:
        trie_root = pickle.load(f)

    tablero = generar_tablero(dados)
    print("\n🔹 Tablero generado:")
    for fila in tablero:
        print(fila)

    modo = input("\n¿Querés jugar (1) o ver el jugador perfecto (2)? ").strip()
    if modo == "2":
        palabras = jugadorPerf(tablero, trie_root)
        print(f"\nPalabras encontradas ({len(palabras)}):")
        for p in palabras:
            print(p)
        print(f"\nPuntaje perfecto: {sum(calcular_puntaje(p) for p in palabras)}")
    else:
        # Tenés que asegurarte que 'diccionario' también lo podás cargar como estructura si no vas a usar Trie con clases
        diccionario = trie_root  # para que funcione la validación en modo jugador
        jugar(tablero, diccionario, tiempo)
