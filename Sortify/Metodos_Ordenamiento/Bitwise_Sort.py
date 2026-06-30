# Animated algorithm (used by the visualization/chart window)
def bitwise_sort(arr, draw_func, delay):
    state = draw_func.state

    if len(arr) == 0:
        return

    max_val = max(arr)
    max_bits = max_val.bit_length()

    def sort_bit(bit_index, i=0, zero_bucket=None, one_bucket=None):
        nonlocal arr

        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
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


# Non-visual algorithm, used for complexity analysis (complexity_window)
def bitwise_sort_estudio(values):
    steps = 0

    if len(values) == 0:
        return steps

    max_val = max(values)
    max_bits = max_val.bit_length()

    for bit_index in range(max_bits):
        zero_bucket = []
        one_bucket = []
        for num in values:
            steps += 1
            if (num >> bit_index) & 1 == 0:
                zero_bucket.append(num)
            else:
                one_bucket.append(num)
        values[:] = zero_bucket + one_bucket
        steps += len(values)

    return steps