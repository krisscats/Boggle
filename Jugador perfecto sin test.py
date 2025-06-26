def qs(L):
    if L == []:
        return []
    menores = []
    mayores = []
    rata = L[0] 
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
