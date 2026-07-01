# Algoritmo con visualización animada (usado en la graficadora)
def bitonic_sort(arr, draw_func, delay):
    estado = draw_func.estado

    def next_power_of_two(n):
        power = 1
        while power < n:
            power *= 2
        return power

    original_len = len(arr)
    target_len = next_power_of_two(original_len)

    temp_arr = arr.copy()
    temp_arr.extend([max(temp_arr)] * (target_len - original_len))

    def compare_and_swap(i, j, direction, callback):
        if estado["valor"] == "detenido":
            return
        elif estado["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: compare_and_swap(i, j, direction, callback))
            return

        if (direction == 1 and temp_arr[i] > temp_arr[j]) or (direction == 0 and temp_arr[i] < temp_arr[j]):
            temp_arr[i], temp_arr[j] = temp_arr[j], temp_arr[i]

        colores = ["orange" if x == i or x == j else "gray" for x in range(original_len)]
        draw_func(temp_arr[:original_len], colores)
        draw_func.canvas.after(int(delay * 100), callback)

    def bitonic_merge(low, count, direction, callback):
        if count > 1:
            k = count // 2
            i = 0

            def merge_step():
                nonlocal i
                if i < k:
                    compare_and_swap(low + i, low + i + k, direction, merge_step)
                    i += 1
                else:
                    bitonic_merge(low, k, direction, lambda: bitonic_merge(low + k, k, direction, callback))

            merge_step()
        else:
            callback()

    def bitonic_sort_recursive(low, count, direction, callback):
        if count > 1:
            k = count // 2
            bitonic_sort_recursive(low, k, 1, lambda:
                bitonic_sort_recursive(low + k, k, 0, lambda:
                    bitonic_merge(low, count, direction, callback)))
        else:
            callback()

    def finalizar():
        for i in range(original_len):
            arr[i] = temp_arr[i]
        draw_func(arr, ["green"] * original_len)

    bitonic_sort_recursive(0, len(temp_arr), 1, finalizar)


# Algoritmo sin visualización, usado para análisis de complejidad (Ventana_Complejidad)
def bitonic_sort_estudio(lista):
    pasos = 0

    def compare_and_swap(i, j, direction):
        nonlocal pasos
        pasos += 1
        if (direction == 1 and lista[i] > lista[j]) or (direction == 0 and lista[i] < lista[j]):
            lista[i], lista[j] = lista[j], lista[i]
            pasos += 1

    def bitonic_merge(low, count, direction):
        if count > 1:
            k = count // 2
            for i in range(low, low + k):
                compare_and_swap(i, i + k, direction)
            bitonic_merge(low, k, direction)
            bitonic_merge(low + k, k, direction)

    def bitonic_sort_recursive(low, count, direction):
        if count > 1:
            k = count // 2
            bitonic_sort_recursive(low, k, 1)
            bitonic_sort_recursive(low + k, k, 0)
            bitonic_merge(low, count, direction)

    def next_power_of_two(n):
        power = 1
        while power < n:
            power *= 2
        return power

    original_len = len(lista)
    target_len = next_power_of_two(original_len)
    lista.extend([max(lista)] * (target_len - original_len))

    bitonic_sort_recursive(0, len(lista), 1)

    del lista[original_len:]

    return pasos

