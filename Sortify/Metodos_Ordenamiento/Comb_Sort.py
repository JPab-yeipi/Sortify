# Algoritmo con visualización animada (usado en la graficadora)
def comb_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False

    def paso():
        nonlocal gap, sorted_flag

        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, paso)
            return

        if gap > 1:
            gap = int(gap / shrink)
        else:
            gap = 1
            sorted_flag = True

        i = 0

        def comparar():
            nonlocal i, sorted_flag
            if estado["valor"] == "detenido":
                return
            elif estado["valor"] == "pausado":
                draw_func.canvas.after(100, comparar)
                return

            if i + gap < n:
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted_flag = False

                draw_func(arr, ["red" if x == i or x == i + gap else "gray" for x in range(n)])
                i += 1
                draw_func.canvas.after(int(delay * 100), comparar)
            else:
                if not sorted_flag or gap != 1:
                    draw_func.canvas.after(1, paso)
                else:
                    draw_func(arr, ["green"] * n)

        comparar()

    paso()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def comb_sort_estudio(lista):
    pasos = 0
    n = len(lista)
    gap = n
    shrink = 1.3

    while True:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        else:
            sorted_flag = False

        i = 0
        while i + gap < n:
            pasos += 1
            if lista[i] > lista[i + gap]:
                lista[i], lista[i + gap] = lista[i + gap], lista[i]
                pasos += 2
                sorted_flag = False
            i += 1

        if gap == 1 and sorted_flag:
            break

    return pasos