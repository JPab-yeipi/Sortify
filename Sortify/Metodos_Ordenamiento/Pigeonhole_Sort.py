# Algoritmo con visualización animada (usado en la graficadora)
def pigeonhole_sort(arr, draw_func, delay):
    estado = draw_func.estado

    if len(arr) == 0:
        return

    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    i_insert = 0
    paso = 0
    total = len(arr)

    def distribuir(paso):
        if paso >= total or estado["valor"] == "detenido":
            rellenar(0, 0)
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: distribuir(paso))
            return

        number = arr[paso]
        holes[number - min_val].append(number)
        draw_func(arr, ["purple" if x == paso else "gray" for x in range(len(arr))])
        draw_func.canvas.after(int(delay * 100), lambda: distribuir(paso + 1))

    def rellenar(h, idx):
        nonlocal i_insert
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: rellenar(h, idx))
            return

        if h < len(holes):
            if idx < len(holes[h]):
                arr[i_insert] = holes[h][idx]
                draw_func(arr, ["green" if x == i_insert else "gray" for x in range(len(arr))])
                i_insert += 1
                draw_func.canvas.after(int(delay * 100), lambda: rellenar(h, idx + 1))
            else:
                draw_func.canvas.after(1, lambda: rellenar(h + 1, 0))
        else:
            draw_func(arr, ["green"] * len(arr))

    distribuir(0)

# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def pigeonhole_sort_estudio(lista):
    pasos = 0

    if len(lista) == 0:
        return pasos

    min_val = min(lista)
    max_val = max(lista)
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]

    for number in lista:
        holes[number - min_val].append(number)
        pasos += 1

    i = 0
    for hole in holes:
        for number in hole:
            lista[i] = number
            pasos += 1
            i += 1

    return pasos
