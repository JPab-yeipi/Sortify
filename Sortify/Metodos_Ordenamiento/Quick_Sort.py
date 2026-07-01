# Algoritmo con visualización animada (usado en la graficadora)
def quick_sort(arr, draw_func, delay):
    estado = draw_func.estado
    stack = [(0, len(arr) - 1)]

    def paso():
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, paso)
            return

        if not stack:
            draw_func(arr, ["green"] * len(arr))
            return

        low, high = stack.pop()

        if low < high:
            i = low - 1
            pivot = arr[high]
            j = low

            def particionar():
                nonlocal i, j
                if estado["valor"] == "detenido":
                    return
                if estado["valor"] == "pausado":
                    draw_func.canvas.after(100, particionar)
                    return

                if j < high:
                    if arr[j] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        draw_func(arr, ["red" if x == i or x == j else "gray" for x in range(len(arr))])
                    j += 1
                    draw_func.canvas.after(int(delay * 100), particionar)
                else:
                    arr[i + 1], arr[high] = arr[high], arr[i + 1]
                    draw_func(arr, ["blue" if x == i + 1 else "gray" for x in range(len(arr))])
                    stack.append((low, i))
                    stack.append((i + 2, high))
                    draw_func.canvas.after(int(delay * 100), paso)

            particionar()
        else:
            draw_func.canvas.after(1, paso)

    paso()


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def quick_sort_estudio(lista):
    pasos = 0

    def partition(low, high):
        nonlocal pasos
        pivot = lista[high]
        i = low - 1

        for j in range(low, high):
            pasos += 1
            if lista[j] <= pivot:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
                pasos += 1

        lista[i + 1], lista[high] = lista[high], lista[i + 1]
        pasos += 1
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(lista) - 1)
    return pasos