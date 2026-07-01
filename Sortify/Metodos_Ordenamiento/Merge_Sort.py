# Algoritmo con visualización animada (usado en la graficadora)
def merge_sort(arr, draw_func, delay):
    estado = draw_func.estado

    def merge_sort_recursive(start, end, callback):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: merge_sort_recursive(start, end, callback))
            return

        if start < end:
            mid = (start + end) // 2
            merge_sort_recursive(start, mid, lambda: merge_sort_recursive(mid + 1, end, lambda: merge(start, mid, end, callback)))
        else:
            draw_func.canvas.after(1, callback)

    def merge(start, mid, end, callback):
        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: merge(start, mid, end, callback))
            return

        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]
        i = j = 0
        k = start

        def merge_step():
            nonlocal i, j, k
            if estado["valor"] == "detenido":
                return
            if estado["valor"] == "pausado":
                draw_func.canvas.after(100, merge_step)
                return

            if i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                draw_func(arr, ["purple" if x == k else "gray" for x in range(len(arr))])
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            elif i < len(left):
                arr[k] = left[i]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(len(arr))])
                i += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            elif j < len(right):
                arr[k] = right[j]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(len(arr))])
                j += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            else:
                draw_func.canvas.after(1, callback)

        merge_step()

    merge_sort_recursive(0, len(arr) - 1, lambda: draw_func(arr, ["green"] * len(arr)))


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def merge_sort_estudio(lista):
    pasos = 0

    def merge(left, right):
        nonlocal pasos
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            pasos += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            pasos += 1

        result.extend(left[i:])
        result.extend(right[j:])
        pasos += len(left[i:]) + len(right[j:])
        return result

    def merge_sort_recursive(sub_arr):
        if len(sub_arr) <= 1:
            return sub_arr

        mid = len(sub_arr) // 2
        left = merge_sort_recursive(sub_arr[:mid])
        right = merge_sort_recursive(sub_arr[mid:])
        return merge(left, right)

    resultado = merge_sort_recursive(lista)
    for i in range(len(lista)):
        lista[i] = resultado[i]
        pasos += 1

    return pasos

