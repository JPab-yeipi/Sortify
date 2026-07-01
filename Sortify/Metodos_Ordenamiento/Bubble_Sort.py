# Algoritmo con visualización animada (usado en la graficadora)
def bubble_sort(arr, draw_func, delay):
    n = len(arr)
    estado = draw_func.estado

    def paso(i, j):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: paso(i, j))
            return

        if i < n - 1:
            if j < n - i - 1:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

                draw_func(arr, ["red" if x == j or x == j + 1 else "gray" for x in range(len(arr))])

                try:
                    draw_func.canvas.after(int(delay * 100), lambda: paso(i, j + 1))
                except Exception as e:
                    print("Se interrumpió la animación:", e)
            else:
                draw_func.canvas.after(1, lambda: paso(i + 1, 0))

    paso(0, 0)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def bubble_sort_estudio(lista):
    pasos = 0
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            pasos += 1
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                pasos += 1
    return pasos