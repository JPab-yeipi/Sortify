# Algoritmo con visualización animada (usado en la graficadora)
def gnome_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)
    index = 0

    def paso():
        nonlocal index

        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, paso)
            return

        if index < n:
            if index == 0:
                index += 1
            elif arr[index] >= arr[index - 1]:
                index += 1
            else:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                draw_func(arr, ["orange" if x == index or x == index - 1 else "gray" for x in range(n)])
                index = max(0, index - 1)
                draw_func.canvas.after(int(delay * 100), paso)
                return

            draw_func(arr, ["green" if x < index else "gray" for x in range(n)])
            draw_func.canvas.after(int(delay * 100), paso)
        else:
            draw_func(arr, ["green"] * n)

    paso()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def gnome_sort_estudio(lista):
    pasos = 0
    n = len(lista)
    index = 0

    while index < n:
        if index == 0:
            index += 1
            pasos += 1
        elif lista[index] >= lista[index - 1]:
            pasos += 1
            index += 1
        else:
            lista[index], lista[index - 1] = lista[index - 1], lista[index]
            pasos += 2
            index = max(0, index - 1)

    return pasos