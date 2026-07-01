# Algoritmo con visualización animada (usado en la graficadora)
def pancake_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)

    def flip(end):
        start = 0
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    def paso(i):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: paso(i))
            return

        if i > 1:
            max_idx = 0
            for j in range(1, i):
                if arr[j] > arr[max_idx]:
                    max_idx = j

            if max_idx != i - 1:
                flip(max_idx)
                draw_func(arr, ["red" if x <= max_idx else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: flip_and_continue(i))
            else:
                draw_func.canvas.after(1, lambda: paso(i - 1))
        else:
            draw_func(arr, ["green"] * n)

    def flip_and_continue(i):
        flip(i - 1)
        draw_func(arr, ["blue" if x < i else "gray" for x in range(n)])
        draw_func.canvas.after(int(delay * 100), lambda: paso(i - 1))

    paso(n)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def pancake_sort_estudio(lista):
    pasos = 0

    def flip(end):
        nonlocal pasos
        start = 0
        while start < end:
            lista[start], lista[end] = lista[end], lista[start]
            pasos += 1
            start += 1
            end -= 1

    n = len(lista)
    for i in range(n, 1, -1):
        max_idx = 0
        for j in range(1, i):
            pasos += 1
            if lista[j] > lista[max_idx]:
                max_idx = j

        if max_idx != i - 1:
            flip(max_idx)
            flip(i - 1)

    return pasos
