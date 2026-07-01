# Algoritmo con visualización animada (usado en la graficadora)
def cocktail_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)
    inicio = 0
    fin = n - 1
    direccion = 1

    def paso(i, ini, fin, dir, cambiado):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: paso(i, ini, fin, dir, cambiado))
            return

        if dir == 1:
            if i < fin:
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    cambiado = True
                draw_func(arr, ["red" if x == i or x == i+1 else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: paso(i + 1, ini, fin, dir, cambiado))
            else:
                if not cambiado:
                    draw_func(arr, ["green"] * n)
                    return
                fin -= 1
                draw_func.canvas.after(1, lambda: paso(fin, ini, fin, -1, False))
        else:
            if i > ini:
                if arr[i] < arr[i - 1]:
                    arr[i], arr[i - 1] = arr[i - 1], arr[i]
                    cambiado = True
                draw_func(arr, ["red" if x == i or x == i-1 else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: paso(i - 1, ini, fin, dir, cambiado))
            else:
                if not cambiado:
                    draw_func(arr, ["green"] * n)
                    return
                ini += 1
                draw_func.canvas.after(1, lambda: paso(ini, ini, fin, 1, False))

    paso(inicio, inicio, fin, direccion, False)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def cocktail_sort_estudio(lista):
    pasos = 0
    n = len(lista)
    inicio = 0
    fin = n - 1
    cambiado = True

    while cambiado:
        cambiado = False

        for i in range(inicio, fin):
            pasos += 1
            if lista[i] > lista[i + 1]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                pasos += 1
                cambiado = True

        fin -= 1

        for i in range(fin, inicio, -1):
            pasos += 1
            if lista[i] < lista[i - 1]:
                lista[i], lista[i - 1] = lista[i - 1], lista[i]
                pasos += 1
                cambiado = True

        inicio += 1

    return pasos