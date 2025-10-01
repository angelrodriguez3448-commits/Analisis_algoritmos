def quick_sort(arr):
    if len(arr) <= 1:
        return arr #Caso base
    
    pivot = arr[len(arr) // 2] #Selcciona el pivote

    left = [x for x in arr if x < pivot] #Elementos menores al pivote
    middle = [x for x in arr if x == pivot] #Elementos iguales al pivote
    right = [x for x in arr if x > pivot] #Elementos mayores al pivote

    return quick_sort(left) + middle + quick_sort(right) #Llamadas recursivas

#Ejemplo de uso:
arr = [7, 38, 27, 3, 9, 82, 10]
sorted_arr = quick_sort(arr)
print("Arreglo ordenado: ", sorted_arr)