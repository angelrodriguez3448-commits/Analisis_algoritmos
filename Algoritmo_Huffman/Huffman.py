from bitstring import BitArray

def huffman_encoding(data):
    # Check for empty input
    if not data:
        return "", None
    frequency = {}
    for char in data:
    # Calculamos la frecuencia de cada caracter
        if char not in frequency:
            frequency[char] = 0
        frequency[char] += 1
    # Create a priority queue
    nodo = [[weight, [char, ""]] for char, weight in frequency.items()]
    while len(nodo) > 1:
        # Ordenamos los nodos por frecuencia
        nodo = sorted(nodo)
        # Tomamos los dos nodos con menor frecuencia
        izquierda = nodo[0]
        derecha = nodo[1]
        for par in izquierda[1:]:
            # agregamos '0' al frente de cada código
            par[1] = '0' + par[1]
        for par in derecha[1:]:
            # agregamos '1' al frente de cada código
            par[1] = '1' + par[1]
        nodo = nodo[2:]
        # combinamos los dos nodo
        nodo.append([izquierda[0] + derecha[0]] + izquierda[1:] + derecha[1:])
    # Creamos la lista de códigos Huffman
    huffman_code = sorted(nodo[0][1:], key=lambda p: (len(p[-1]), p))
    # Lo convertimos en un diccionario
    huffman_diccionario = {char: code for char, code in huffman_code}
    return huffman_diccionario

def compresion(data, huffman_diccionario):
    # Codificamos la data usando el diccionario de Huffman
    data_codificada = ''.join(huffman_diccionario[char] for char in data)

    # Convertimos la cadena binaria en un objeto BitArray
    bit_array = BitArray(bin=data_codificada)
    return bit_array

def descompresion(bit_array, huffman_diccionario):
    # Creamos un diccionario inverso
    diccionario_inverso = {codigo: char for char, codigo in huffman_diccionario.items()}

    # Convertimos el BitArray a una cadena binaria
    data_codificada = bit_array.bin

    codigo_actual = ""
    data_decodificada = ""

    # Decodificamos la cadena binaria a cadena de caracteres con el diccionario inverso
    for bit in data_codificada:
        codigo_actual += bit
        if codigo_actual in diccionario_inverso:
            data_decodificada += diccionario_inverso[codigo_actual]
            codigo_actual = ""
    return data_decodificada


