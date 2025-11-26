# -------------------------------------------
# Proyecto: Divide y Vencerás - NCBI DNA Search
# Autor: Arturo Morales Pedroza
# -------------------------------------------

from Bio import Entrez, SeqIO
import time
import matplotlib.pyplot as plt

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


# ------------------------------------------------------
# ALGORITMOS DE BÚSQUEDA
# ------------------------------------------------------

def naive_search(text, pattern):
    """Fuerza Bruta: busca todas las ocurrencias del patrón en el texto."""
    n, m = len(text), len(pattern)
    matches = []
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            matches.append(i)
    return matches

def divide_and_conquer_search(text, pattern, start=0):
    """Versión Divide y Vencerás del Naive String Matching."""
    n, m = len(text), len(pattern)
    if n < m:
        return []
    elif n <= 2 * m:
        return [start + i for i in range(n - m + 1) if text[i:i+m] == pattern]
    else:
        mid = n // 2
        left = divide_and_conquer_search(text[:mid + m - 1], pattern, start)
        right = divide_and_conquer_search(text[mid:], pattern, start + mid)
        return left + right

# ------------------------------------------------------
# COMPARATIVA DE DESEMPEÑO
# ------------------------------------------------------

def medir_tiempo(algoritmo, texto, patron):
    inicio = time.time()
    algoritmo(texto, patron)
    return time.time() - inicio


def comparar_algoritmos(texto, patron):
    tamaños = [len(texto)//20, len(texto)//10, len(texto)//5, len(texto)//2, len(texto)]
    tiempos_naive, tiempos_divide = [], []

    for t in tamaños:
        subtexto = texto[:t]
        tiempos_naive.append(medir_tiempo(naive_search, subtexto, patron))
        tiempos_divide.append(medir_tiempo(divide_and_conquer_search, subtexto, patron))

    plt.plot(tamaños, tiempos_naive, label="Naive", marker='o')
    plt.plot(tamaños, tiempos_divide, label="Divide y Vencerás", marker='s')
    plt.xlabel("Tamaño del texto (bases)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparativa de rendimiento: Naive vs Divide y Vencerás")
    plt.legend()
    plt.grid(True)
    plt.show()


# ------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------

if __name__ == "__main__":

    id_secuencia = "NC_045512.2"  # SARS-CoV-2
    secuencia = obtener_secuencia_ncbi(id_secuencia)
    print(secuencia)

    # Ejemplo de patrón a buscar
    patron = "ATGTTTGTTT"

    print("\n=== Búsqueda Naive ===")
    resultados_naive = naive_search(secuencia, patron)
    print(f"Coincidencias encontradas: {len(resultados_naive)} \n en posiciones: {resultados_naive}")

    print("\n=== Búsqueda Divide y Vencerás ===")
    resultados_divide = divide_and_conquer_search(secuencia, patron)
    print(f"Coincidencias encontradas: {len(resultados_divide)} \n en posiciones: {resultados_divide}")

    # Comparativa de tiempos
    comparar_algoritmos(secuencia, patron)
