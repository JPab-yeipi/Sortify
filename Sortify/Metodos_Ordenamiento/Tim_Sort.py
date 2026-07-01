# Algoritmo con visualización animada (usado en la graficadora)
def tim_sort(arr, draw_func, delay):
    estado = draw_func.estado
    MIN_RUN = 32
    n = len(arr)

    def insertion_sort(start, end, callback):
        def paso(i):
            if estado["valor"] == "detenido":
                return
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
                    draw_func(arr, ["orange" if x == j_interno or x == i else "gray" for x in range(n)])
                    draw_func.canvas.after(int(delay * 100), lambda: mover(j_interno - 1))
                else:
                    arr[j_interno + 1] = key
                    draw_func(arr, ["green" if start <= x <= i else "gray" for x in range(n)])
                    draw_func.canvas.after(int(delay * 100), lambda: paso(i + 1))

            mover(j)

        paso(start + 1)

    def merge(left, mid, right, callback):
        len1, len2 = mid - left + 1, right - mid
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        def merge_paso():
            nonlocal i, j, k
            if estado["valor"] == "detenido":
                return
            if estado["valor"] == "pausado":
                draw_func.canvas.after(100, merge_paso)
                return

            if i < len1 and j < len2:
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                draw_func(arr, ["purple" if x == k else "gray" for x in range(n)])
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_paso)
            elif i < len1:
                arr[k] = left_part[i]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(n)])
                i += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_paso)
            elif j < len2:
                arr[k] = right_part[j]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(n)])
                j += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_paso)
            else:
                callback()

        merge_paso()

    def ordenar_bloques(inicio):
        if inicio >= n:
            mezclar(32)
            return
        fin = min(inicio + MIN_RUN - 1, n - 1)
        insertion_sort(inicio, fin, lambda: ordenar_bloques(inicio + MIN_RUN))

    def mezclar(tam_actual):
        if tam_actual >= n:
            draw_func(arr, ["green"] * n)
            return

        merges = []

        for left in range(0, n, 2 * tam_actual):
            mid = min(n - 1, left + tam_actual - 1)
            right = min((left + 2 * tam_actual - 1), n - 1)
            if mid < right:
                merges.append((left, mid, right))

        def aplicar_merge(i):
            if i < len(merges):
                l, m, r = merges[i]
                merge(l, m, r, lambda: aplicar_merge(i + 1))
            else:
                mezclar(tam_actual * 2)

        aplicar_merge(0)

    ordenar_bloques(0)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def tim_sort_estudio(lista):
    pasos = 0
    MIN_RUN = 32
    n = len(lista)

    def insertion_sort(start, end):
        nonlocal pasos
        for i in range(start + 1, end + 1):
            key = lista[i]
            j = i - 1
            while j >= start and lista[j] > key:
                lista[j + 1] = lista[j]
                j -= 1
                pasos += 2
            lista[j + 1] = key
            pasos += 1

    def merge(left, mid, right):
        nonlocal pasos
        left_part = lista[left:mid + 1]
        right_part = lista[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            pasos += 1
            if left_part[i] <= right_part[j]:
                lista[k] = left_part[i]
                i += 1
            else:
                lista[k] = right_part[j]
                j += 1
            pasos += 1
            k += 1

        while i < len(left_part):
            lista[k] = left_part[i]
            i += 1
            k += 1
            pasos += 1

        while j < len(right_part):
            lista[k] = right_part[j]
            j += 1
            k += 1
            pasos += 1

    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        insertion_sort(start, end)

    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), n - 1)
            if mid < right:
                merge(left, mid, right)
        size *= 2

    return pasos
