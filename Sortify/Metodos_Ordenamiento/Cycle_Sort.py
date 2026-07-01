# Algoritmo con visualización animada (usado en la graficadora)
def cycle_sort(arr, draw_func, delay):
    estado = draw_func.estado
    n = len(arr)

    def ciclo(cycle_start):
        if cycle_start >= n - 1 or estado["valor"] == "detenido":
            draw_func(arr, ["green"] * n)
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: ciclo(cycle_start))
            return

        item = arr[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            draw_func.canvas.after(1, lambda: ciclo(cycle_start + 1))
            return

        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        draw_func(arr, ["orange" if x == pos else "gray" for x in range(n)])

        def continuar(pos_actual, item_actual):
            if estado["valor"] == "detenido":
                return
            if estado["valor"] == "pausado":
                draw_func.canvas.after(100, lambda: continuar(pos_actual, item_actual))
                return

            new_pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item_actual:
                    new_pos += 1

            while item_actual == arr[new_pos]:
                new_pos += 1

            if new_pos >= len(arr):
                draw_func.canvas.after(1, lambda: ciclo(cycle_start + 1))
                return

            arr[new_pos], item_actual = item_actual, arr[new_pos]
            draw_func(arr, ["red" if x == new_pos else "gray" for x in range(n)])

            if new_pos != cycle_start:
                draw_func.canvas.after(int(delay * 100), lambda: continuar(new_pos, item_actual))
            else:
                draw_func.canvas.after(int(delay * 100), lambda: ciclo(cycle_start + 1))

        draw_func.canvas.after(int(delay * 100), lambda: continuar(pos, item))

    ciclo(0)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def cycle_sort_estudio(lista):
    pasos = 0
    n = len(lista)

    for cycle_start in range(n - 1):
        item = lista[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, n):
            pasos += 1
            if lista[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == lista[pos]:
            pos += 1
            pasos += 1

        if pos < n:
            lista[pos], item = item, lista[pos]
            pasos += 1

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                pasos += 1
                if lista[i] < item:
                    pos += 1

            while pos < n and item == lista[pos]:
                pos += 1
                pasos += 1

            if pos < n:
                lista[pos], item = item, lista[pos]
                pasos += 1

    return pasos