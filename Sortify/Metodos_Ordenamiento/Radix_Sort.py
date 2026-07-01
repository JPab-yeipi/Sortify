# Algoritmo con visualización animada (usado en la graficadora)
def radix_sort(arr, draw_func, delay):
    estado = draw_func.estado

    if len(arr) == 0:
        return

    max_num = max(arr)
    exp = 1

    def counting_sort_by_digit(exp, i=0, fase="contar", count=None, output=None):
        n = len(arr)
        if count is None:
            count = [0] * 10
            output = [0] * n

        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: counting_sort_by_digit(exp, i, fase, count, output))
            return

        if fase == "contar":
            if i < n:
                index = arr[i] // exp
                count[index % 10] += 1
                draw_func(arr, ["orange" if x == i else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: counting_sort_by_digit(exp, i + 1, "contar", count, output))
            else:
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, 1, "acumular", count, output))

        elif fase == "acumular":
            if i < 10:
                count[i] += count[i - 1]
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, i + 1, "acumular", count, output))
            else:
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, n - 1, "ordenar", count, output))

        elif fase == "ordenar":
            if i >= 0:
                index = arr[i] // exp
                output[count[index % 10] - 1] = arr[i]
                count[index % 10] -= 1
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, i - 1, "ordenar", count, output))
            else:
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, 0, "reescribir", count, output))

        elif fase == "reescribir":
            if i < n:
                arr[i] = output[i]
                draw_func(arr, ["blue" if x == i else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: counting_sort_by_digit(exp, i + 1, "reescribir", count, output))
            else:
                siguiente_exp(exp)

    def siguiente_exp(exp_actual):
        siguiente = exp_actual * 10
        if max_num // siguiente > 0:
            counting_sort_by_digit(siguiente)
        else:
            draw_func(arr, ["green"] * len(arr))

    counting_sort_by_digit(exp)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def radix_sort_estudio(lista):
    pasos = 0
    if len(lista) == 0:
        return pasos

    max_num = max(lista)
    exp = 1
    n = len(lista)

    while max_num // exp > 0:
        count = [0] * 10
        output = [0] * n

        for i in range(n):
            index = lista[i] // exp
            count[index % 10] += 1
            pasos += 1

        for i in range(1, 10):
            count[i] += count[i - 1]
            pasos += 1

        for i in range(n - 1, -1, -1):
            index = lista[i] // exp
            output[count[index % 10] - 1] = lista[i]
            count[index % 10] -= 1
            pasos += 2

        for i in range(n):
            lista[i] = output[i]
            pasos += 1

        exp *= 10

    return pasos
