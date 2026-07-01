# Algoritmo con visualización animada (usado en la graficadora)
def bitwise_sort(arr, draw_func, delay):
    estado = draw_func.estado

    if len(arr) == 0:
        return

    max_val = max(arr)
    max_bits = max_val.bit_length()

    def sort_bit(bit_index, i=0, zero_bucket=None, one_bucket=None):
        nonlocal arr

        if estado["valor"] == "detenido":
            return
        if estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: sort_bit(bit_index, i, zero_bucket, one_bucket))
            return

        if zero_bucket is None:
            zero_bucket = []
            one_bucket = []

        if i < len(arr):
            if (arr[i] >> bit_index) & 1 == 0:
                zero_bucket.append(arr[i])
            else:
                one_bucket.append(arr[i])
            draw_func(arr, ["orange" if x == i else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: sort_bit(bit_index, i + 1, zero_bucket, one_bucket))
        else:
            arr[:] = zero_bucket + one_bucket
            draw_func(arr, ["blue"] * len(arr))
            if bit_index + 1 < max_bits:
                draw_func.canvas.after(int(delay * 100), lambda: sort_bit(bit_index + 1))
            else:
                draw_func(arr, ["green"] * len(arr))

    sort_bit(0)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def bitwise_sort_estudio(lista):
    pasos = 0

    if len(lista) == 0:
        return pasos

    max_val = max(lista)
    max_bits = max_val.bit_length()

    for bit_index in range(max_bits):
        zero_bucket = []
        one_bucket = []
        for num in lista:
            pasos += 1
            if (num >> bit_index) & 1 == 0:
                zero_bucket.append(num)
            else:
                one_bucket.append(num)
        lista[:] = zero_bucket + one_bucket
        pasos += len(lista)

    return pasos
