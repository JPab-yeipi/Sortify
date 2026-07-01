# Algoritmo con visualización animada (usado en la graficadora)
def bucket_sort(arr, draw_func, delay):
    estado = draw_func.estado

    if len(arr) == 0:
        return

    max_val = max(arr)
    size = max_val / len(arr)
    buckets = [[] for _ in range(len(arr))]

    i_insert = 0

    def colocar_en_buckets(i):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: colocar_en_buckets(i))
            return

        if i < len(arr):
            num = arr[i]
            index = int(num / size)
            if index != len(arr):
                buckets[index].append(num)
            else:
                buckets[len(arr) - 1].append(num)

            draw_func(arr, ["blue" if x == i else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: colocar_en_buckets(i + 1))
        else:
            ordenar_buckets(0, 0)

    def ordenar_buckets(b, pos):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: ordenar_buckets(b, pos))
            return

        nonlocal i_insert

        if b < len(buckets):
            bucket = sorted(buckets[b])
            if pos < len(bucket):
                arr[i_insert] = bucket[pos]
                draw_func(arr, ["green" if x == i_insert else "gray" for x in range(len(arr))])
                i_insert += 1
                draw_func.canvas.after(int(delay * 100), lambda: ordenar_buckets(b, pos + 1))
            else:
                draw_func.canvas.after(1, lambda: ordenar_buckets(b + 1, 0))
        else:
            draw_func(arr, ["green"] * len(arr))

    colocar_en_buckets(0)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def bucket_sort_estudio(lista):
    pasos = 0

    if len(lista) == 0:
        return pasos

    max_val = max(lista)
    size = max_val / len(lista)
    buckets = [[] for _ in range(len(lista))]

    for num in lista:
        index = int(num / size)
        if index != len(lista):
            buckets[index].append(num)
        else:
            buckets[len(lista) - 1].append(num)
        pasos += 1

    i = 0
    for bucket in buckets:
        bucket.sort()
        for num in bucket:
            lista[i] = num
            pasos += 1
            i += 1

    return pasos
