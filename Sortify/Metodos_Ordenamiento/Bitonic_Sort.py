# Animated algorithm (used by the visualization/chart window)
def bitonic_sort(arr, draw_func, delay):
    state = draw_func.state

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
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, lambda: compare_and_swap(i, j, direction, callback))
            return

        if (direction == 1 and temp_arr[i] > temp_arr[j]) or (direction == 0 and temp_arr[i] < temp_arr[j]):
            temp_arr[i], temp_arr[j] = temp_arr[j], temp_arr[i]

        colors = ["orange" if x == i or x == j else "gray" for x in range(original_len)]
        draw_func(temp_arr[:original_len], colors)
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

    def finalize():
        for i in range(original_len):
            arr[i] = temp_arr[i]
        draw_func(arr, ["green"] * original_len)

    bitonic_sort_recursive(0, len(temp_arr), 1, finalize)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def bitonic_sort_estudio(values):
    steps = 0

    def compare_and_swap(i, j, direction):
        nonlocal steps
        steps += 1
        if (direction == 1 and values[i] > values[j]) or (direction == 0 and values[i] < values[j]):
            values[i], values[j] = values[j], values[i]
            steps += 1

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

    original_len = len(values)
    target_len = next_power_of_two(original_len)
    values.extend([max(values)] * (target_len - original_len))

    bitonic_sort_recursive(0, len(values), 1)

    del values[original_len:]

    return steps