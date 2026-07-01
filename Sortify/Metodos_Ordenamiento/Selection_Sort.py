# Algoritmo con visualización animada (usado en la graficadora)
def selection_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)
    i = 0

    def paso_externo():
        nonlocal i
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, paso_externo)
            return
        if i >= n:
            draw_func(arr, ["green"] * n)
            return

        min_idx = i
        j = i + 1

        def buscar_minimo():
            nonlocal j, min_idx, i
            if estado["valor"] == "detenido":
                return
            if estado["valor"] == "pausado":
                draw_func.canvas.after(100, buscar_minimo)
                return

            if j < n:
                if arr[j] < arr[min_idx]:
                    min_idx = j
                draw_func(arr, [
                    "red" if x == j else
                    "yellow" if x == min_idx else
                    "green" if x < i else "gray" for x in range(n)
                ])
                j += 1
                draw_func.canvas.after(int(delay * 100), buscar_minimo)
            else:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                draw_func(arr, ["green" if x <= i else "gray" for x in range(n)])
                i += 1
                draw_func.canvas.after(int(delay * 100), paso_externo)

        buscar_minimo()

    paso_externo()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def selection_sort_estudio(lista):
    pasos = 0
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            pasos += 1
            if lista[j] < lista[min_idx]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
        pasos += 1
    return pasos