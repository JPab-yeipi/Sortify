# Algoritmo con visualización animada (usado en la graficadora)
def insertion_sort(arr, draw_func, delay):
    estado = draw_func.estado

    def paso(i):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: paso(i))
            return

        if i < len(arr):
            key = arr[i]
            j = i - 1

            def mover(j_interno):
                if estado["valor"] == "detenido":
                    return
                elif estado["valor"] == "pausado":
                    draw_func.canvas.after(100, lambda: mover(j_interno))
                    return

                if j_interno >= 0 and arr[j_interno] > key:
                    arr[j_interno + 1] = arr[j_interno]
                    draw_func(arr, ["orange" if x == j_interno or x == i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: mover(j_interno - 1))
                else:
                    arr[j_interno + 1] = key
                    draw_func(arr, ["green" if x <= i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: paso(i + 1))

            mover(j)
        else:
            draw_func(arr, ["green"] * len(arr))

    paso(1)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def insertion_sort_estudio(lista):
    pasos = 0
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1

        while j >= 0:
            pasos += 1
            if lista[j] > key:
                lista[j + 1] = lista[j]
                pasos += 1
                j -= 1
            else:
                break

        lista[j + 1] = key
        pasos += 1

    return pasos
