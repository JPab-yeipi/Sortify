# Algoritmo con visualización animada (usado en la graficadora)
def counting_sort(arr, draw_func, delay):
    estado = draw_func.estado

    if len(arr) == 0:
        return

    max_val = max(arr)
    min_val = min(arr)
    rango = max_val - min_val + 1

    count = [0] * rango
    output = [0] * len(arr)

    i = 0

    def contar():
        nonlocal i
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, contar)
            return

        if i < len(arr):
            num = arr[i]
            count[num - min_val] += 1
            draw_func(arr, ["purple" if x == i else "gray" for x in range(len(arr))])
            i += 1
            draw_func.canvas.after(int(delay * 100), contar)
        else:
            acumular(1)

    def acumular(j):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: acumular(j))
            return

        if j < len(count):
            count[j] += count[j - 1]
            draw_func.canvas.after(1, lambda: acumular(j + 1))
        else:
            llenar_salida(len(arr) - 1)

    def llenar_salida(k):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: llenar_salida(k))
            return

        if k >= 0:
            num = arr[k]
            index = count[num - min_val] - 1
            output[index] = num
            count[num - min_val] -= 1
            draw_func(output, ["blue" if x == index else "gray" for x in range(len(output))])
            draw_func.canvas.after(int(delay * 100), lambda: llenar_salida(k - 1))
        else:
            escribir_final(0)

    def escribir_final(i):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: escribir_final(i))
            return

        if i < len(arr):
            arr[i] = output[i]
            draw_func(arr, ["green" if x == i else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: escribir_final(i + 1))
        else:
            draw_func(arr, ["green"] * len(arr))

    contar()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def counting_sort_estudio(lista):
    pasos = 0

    if len(lista) == 0:
        return pasos

    max_val = max(lista)
    min_val = min(lista)
    rango = max_val - min_val + 1

    count = [0] * rango
    output = [0] * len(lista)

    for num in lista:
        count[num - min_val] += 1
        pasos += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]
        pasos += 1

    for num in reversed(lista):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
        pasos += 2

    for i in range(len(lista)):
        lista[i] = output[i]
        pasos += 1

    return pasos
