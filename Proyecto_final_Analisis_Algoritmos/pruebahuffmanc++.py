import heapq
import sys
sys.path.append("/home/gavos/Proyecto_final_Analisis_Algoritmos/build/lib.linux-x86_64-cpython-39")
import busqueda
import time
from bitarray import bitarray
from Bio import Entrez, SeqIO

# CONFIGURACIÓN DE NCBI
Entrez.email = "arturo.morales7406@alumnos.udg.mx"

# ------------------------------------------------------
# FUNCIÓN PARA DESCARGAR SECUENCIA DE ADN DESDE NCBI
# ------------------------------------------------------
def obtener_secuencia_ncbi(id_ncbi):
    """
    Descarga una secuencia de ADN desde NCBI dado su identificador (por ejemplo: 'NC_045512.2').
    Devuelve la secuencia como una cadena (string).
    """
    print(f"Descargando secuencia {id_ncbi} desde NCBI...")
    handle = Entrez.efetch(db="nucleotide", id=id_ncbi, rettype="fasta", retmode="text")
    registro = SeqIO.read(handle, "fasta")
    handle.close()
    print(f"Secuencia descargada: {len(registro.seq)} bases.")
    return str(registro.seq)

def huffman_encoding(data):
    freq = {}
    for ch in data:
        freq[ch] = freq.get(ch, 0) + 1
    heap = [[w, [ch, ""]] for ch, w in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        for p in left[1:]:
            p[1] = '0' + p[1]
        for p in right[1:]:
            p[1] = '1' + p[1]
        heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])
    return {ch: code for ch, code in heap[0][1:]}

def compresion(data, diccionario):
    bin_str = ''.join(diccionario[ch] for ch in data)
    bit_pack = bitarray(bin_str)
    return bit_pack

def divide_and_conquer_search(text_bin, pattern_bin, start=0):
    """Versión Divide y Vencerás del Naive String Matching."""
    n, m = len(text_bin), len(pattern_bin)
    #text_bin = BitArray(bin=text)
    #pattern_bin = BitArray(bin=pattern)
    if n < m:
        return []
    elif n <= 2 * m:
        return [start + i for i in range(n - m + 1) if text_bin[i:i+m] == pattern_bin]
    else:
        mid = n // 2
        left = divide_and_conquer_search(text_bin[:mid + m - 1], pattern_bin, start)
        right = divide_and_conquer_search(text_bin[mid:], pattern_bin, start + mid)
        return left + right

def naive_search(text, pattern):
    """Fuerza Bruta: busca todas las ocurrencias del patrón en el texto."""
    n, m = len(text), len(pattern)
    matches = []
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            matches.append(i)
    return matches

id_secuencia = "NC_045512.2"  # SARS-CoV-2
secuencia = obtener_secuencia_ncbi(id_secuencia)

patron = "ATGTTTGTTT"
#patron = "ATGT"

diccionario = huffman_encoding(secuencia + patron)
bit_grande = compresion(secuencia, diccionario)
bit_patron = compresion(patron, diccionario)

data_bytes = bit_grande.tobytes()
pattern_bytes = bit_patron.tobytes()

"""start_time1 = time.time()
posiciones = naive_search(bit_grande, bit_patron)
end_time1 = time.time()

print("Busqueda en cadena comprimida (Python)")
print(f"Se encontró el patrón {len(posiciones)} veces en posiciones: {posiciones[:10]}...")
print(f"Tiempo de búsqueda: {end_time1 - start_time1:.6f} segundos")"""

start_time1 = time.time()
posiciones = busqueda.buscar_patron_binario(list(data_bytes), list(pattern_bytes), len(bit_patron))
end_time1 = time.time()

print("Busqueda en cadena comprimida (C++)")
print(f"Se encontró el patrón {len(posiciones)} veces en posiciones: {posiciones[:10]}...")
print(f"Tiempo de búsqueda: {end_time1 - start_time1:.6f} segundos")

"""start_time1 = time.time()
posiciones = divide_and_conquer_search(bit_grande, bit_patron)
end_time1 = time.time()

print("Busqueda en cadena comprimda (divide y venceras)")
print(f"Se encontró el patrón {len(posiciones)} veces en posiciones: {posiciones[:10]}...")
print(f"Tiempo de búsqueda: {end_time1 - start_time1:.6f} segundos")"""