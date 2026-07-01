# Algoritmo con visualización animada (usado en la graficadora)
def heap_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)
    i_build = n // 2 - 1
    i_extract = n - 1

    def heapify(n, i, callback):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: heapify(n, i, callback))
            return

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            draw_func(arr, ["red" if x == i or x == largest else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: heapify(n, largest, callback))
        else:
            draw_func.canvas.after(1, callback)

    def construir_heap():
        nonlocal i_build
        if i_build >= 0:
            heapify(n, i_build, lambda: construir_heap_step())
        else:
            extraer()

    def construir_heap_step():
        nonlocal i_build
        i_build -= 1
        draw_func.canvas.after(1, construir_heap)

    def extraer():
        nonlocal i_extract
        if i_extract > 0:
            arr[i_extract], arr[0] = arr[0], arr[i_extract]
            draw_func(arr, ["green" if x >= i_extract else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: heapify(i_extract, 0, lambda: extraer_step()))
        else:
            draw_func(arr, ["green"] * n)

    def extraer_step():
        nonlocal i_extract
        i_extract -= 1
        draw_func.canvas.after(1, extraer)

    construir_heap()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def heap_sort_estudio(lista):
    pasos = 0

    def heapify(n, i):
        nonlocal pasos
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Comparar con hijo izquierdo
        if left < n:
            pasos += 1  # Comparación por índice
            pasos += 1  # Comparación de valores
            if lista[left] > lista[largest]:
                largest = left
        else:
            pasos += 1  # Comparación fallida por índice

        # Comparar con hijo derecho
        if right < n:
            pasos += 1
            pasos += 1
            if lista[right] > lista[largest]:
                largest = right
        else:
            pasos += 1

        # Si hay que intercambiar
        if largest != i:
            lista[i], lista[largest] = lista[largest], lista[i]
            pasos += 1  # Intercambio
            heapify(n, largest)  # Recursivo

    n = len(lista)

    # Construcción del heap
    for i in range(n // 2 - 1, -1, -1):
        pasos += 1  # Paso de control
        heapify(n, i)

    # Extracción del máximo y reheapify
    for i in range(n - 1, 0, -1):
        lista[i], lista[0] = lista[0], lista[i]
        pasos += 1  # Intercambio
        heapify(i, 0)

    return pasos
