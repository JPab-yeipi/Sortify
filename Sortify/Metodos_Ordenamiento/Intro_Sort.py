# Algoritmo con visualización animada (usado en la graficadora)
def intro_sort(arr, draw_func, delay):
    import math
    estado = draw_func.estado
    n = len(arr)

    def insertion_sort(start, end, callback):
        def paso(i):
            if i > end:
                callback()
                return
            key = arr[i]
            j = i - 1

            def mover(j_interno):
                if estado["valor"] == "detenido":
                    return
                if estado["valor"] == "pausado":
                    draw_func.canvas.after(100, lambda: mover(j_interno))
                    return

                if j_interno >= start and arr[j_interno] > key:
                    arr[j_interno + 1] = arr[j_interno]
                    draw_func(arr, ["orange" if x == j_interno or x == i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: mover(j_interno - 1))
                else:
                    arr[j_interno + 1] = key
                    draw_func(arr, ["green" if x <= i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: paso(i + 1))

            mover(j)

        paso(start + 1)

    def heapify(n, i, offset, callback):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: heapify(n, i, offset, callback))
            return

        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[offset + l] > arr[offset + largest]:
            largest = l
        if r < n and arr[offset + r] > arr[offset + largest]:
            largest = r

        if largest != i:
            arr[offset + i], arr[offset + largest] = arr[offset + largest], arr[offset + i]
            draw_func(arr, ["red" if x == offset + i or x == offset + largest else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: heapify(n, largest, offset, callback))
        else:
            draw_func.canvas.after(1, callback)

    def heap_sort(start, end, callback):
        n = end - start + 1
        i_build = n // 2 - 1
        i_extract = n - 1

        def build():
            nonlocal i_build
            if i_build >= 0:
                heapify(n, i_build, start, lambda: step_build())
            else:
                extract()

        def step_build():
            nonlocal i_build
            i_build -= 1
            draw_func.canvas.after(1, build)

        def extract():
            nonlocal i_extract
            if i_extract > 0:
                arr[start + i_extract], arr[start] = arr[start], arr[start + i_extract]
                draw_func(arr, ["blue" if x == start + i_extract else "gray" for x in range(len(arr))])
                draw_func.canvas.after(int(delay * 100), lambda: heapify(i_extract, 0, start, step_extract))
            else:
                callback()

        def step_extract():
            nonlocal i_extract
            i_extract -= 1
            draw_func.canvas.after(1, extract)

        build()

    def quick_sort(start, end, depth_limit, callback):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: quick_sort(start, end, depth_limit, callback))
            return

        size = end - start + 1
        if size <= 16:
            insertion_sort(start, end, callback)
            return
        if depth_limit == 0:
            heap_sort(start, end, callback)
            return

        pivot = arr[end]
        i = start - 1
        j = start

        def partition_step():
            nonlocal i, j
            if j < end:
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    draw_func(arr, ["red" if x == i or x == j else "gray" for x in range(len(arr))])
                j += 1
                draw_func.canvas.after(int(delay * 100), partition_step)
            else:
                arr[i + 1], arr[end] = arr[end], arr[i + 1]
                p = i + 1
                quick_sort(start, p - 1, depth_limit - 1, lambda: quick_sort(p + 1, end, depth_limit - 1, callback))

        partition_step()

    depth_limit = 2 * math.floor(math.log2(len(arr))) if len(arr) > 0 else 0

    quick_sort(0, len(arr) - 1, depth_limit, lambda: draw_func(arr, ["green"] * len(arr)))


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def intro_sort_estudio(lista):
    import math
    pasos = 0

    def insertion_sort(start, end):
        nonlocal pasos
        for i in range(start + 1, end + 1):
            key = lista[i]
            j = i - 1
            while j >= start and lista[j] > key:
                pasos += 1
                lista[j + 1] = lista[j]
                pasos += 1
                j -= 1
            lista[j + 1] = key
            pasos += 1

    def heapify(n, i, offset):
        nonlocal pasos
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        pasos += 1
        if l < n and lista[offset + l] > lista[offset + largest]:
            largest = l

        pasos += 1
        if r < n and lista[offset + r] > lista[offset + largest]:
            largest = r

        if largest != i:
            lista[offset + i], lista[offset + largest] = lista[offset + largest], lista[offset + i]
            pasos += 1
            heapify(n, largest, offset)

    def heap_sort(start, end):
        nonlocal pasos
        n = end - start + 1
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i, start)
        for i in range(n - 1, 0, -1):
            lista[start + i], lista[start] = lista[start], lista[start + i]
            pasos += 1
            heapify(i, 0, start)

    def quick_sort(start, end, depth_limit):
        nonlocal pasos
        size = end - start + 1
        if size <= 16:
            insertion_sort(start, end)
            return
        if depth_limit == 0:
            heap_sort(start, end)
            return

        pivot = lista[end]
        i = start - 1
        for j in range(start, end):
            pasos += 1
            if lista[j] <= pivot:
                i += 1
                lista[i], lista[j] = lista[j], lista[i]
                pasos += 1

        lista[i + 1], lista[end] = lista[end], lista[i + 1]
        pasos += 1
        p = i + 1

        quick_sort(start, p - 1, depth_limit - 1)
        quick_sort(p + 1, end, depth_limit - 1)

    depth_limit = 2 * math.floor(math.log2(len(lista))) if len(lista) > 0 else 0
    quick_sort(0, len(lista) - 1, depth_limit)

    return pasos
