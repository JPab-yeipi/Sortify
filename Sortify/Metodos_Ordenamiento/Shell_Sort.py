# Algoritmo con visualización animada (usado en la graficadora)
def shell_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2

    i_gap = 0
    i = 0
    j = 0
    temp = None
    fase = "inicio"

    def paso():
        nonlocal i_gap, i, j, temp, fase

        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, paso)
            return

        if i_gap >= len(gaps):
            draw_func(arr, ["green"] * n)
            return

        gap = gaps[i_gap]

        if fase == "inicio":
            if i >= n:
                i_gap += 1
                if i_gap < len(gaps):
                    gap = gaps[i_gap]
                    i = gap
                    fase = "inicio"
                    draw_func.canvas.after(1, paso)
                else:
                    draw_func(arr, ["green"] * n)
                return
            temp = arr[i]
            j = i
            fase = "comparando"
            draw_func.canvas.after(1, paso)

        elif fase == "comparando":
            if j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                draw_func(arr, ["orange" if x == j or x == j - gap else "gray" for x in range(n)])
                j -= gap
                draw_func.canvas.after(int(delay * 100), paso)
            else:
                fase = "insertando"
                draw_func.canvas.after(1, paso)

        elif fase == "insertando":
            arr[j] = temp
            draw_func(arr, ["green" if x == j else "gray" for x in range(n)])
            i += 1
            fase = "inicio"
            draw_func.canvas.after(int(delay * 100), paso)

    i = gaps[0] if gaps else 0
    paso()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def shell_sort_estudio(lista):
    pasos = 0
    n = len(lista)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            pasos += 1

            temp = lista[i]
            j = i

            while j >= gap:
                pasos += 1
                if lista[j - gap] > temp:
                    lista[j] = lista[j - gap]
                    pasos += 1
                    j -= gap
                else:
                    break

            lista[j] = temp
            pasos += 1

        gap //= 2

    return pasos
