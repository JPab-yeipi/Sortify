# Animated algorithm (used by the visualization/chart window)
def counting_sort(arr, draw_func, delay):
    state = draw_func.state

    if len(arr) == 0:
        return

    max_val = max(arr)
    min_val = min(arr)
    value_range = max_val - min_val + 1

    count = [0] * value_range
    output = [0] * len(arr)

    i = 0

    def count_step():
        nonlocal i
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, count_step)
            return

        if i < len(arr):
            num = arr[i]
            count[num - min_val] += 1
            draw_func(arr, ["purple" if x == i else "gray" for x in range(len(arr))])
            i += 1
            draw_func.canvas.after(int(delay * 100), count_step)
        else:
            accumulate(1)

    def accumulate(j):
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, lambda: accumulate(j))
            return

        if j < len(count):
            count[j] += count[j - 1]
            draw_func.canvas.after(1, lambda: accumulate(j + 1))
        else:
            fill_output(len(arr) - 1)

    def fill_output(k):
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, lambda: fill_output(k))
            return

        if k >= 0:
            num = arr[k]
            index = count[num - min_val] - 1
            output[index] = num
            count[num - min_val] -= 1
            draw_func(output, ["blue" if x == index else "gray" for x in range(len(output))])
            draw_func.canvas.after(int(delay * 100), lambda: fill_output(k - 1))
        else:
            write_final(0)

    def write_final(i):
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, lambda: write_final(i))
            return

        if i < len(arr):
            arr[i] = output[i]
            draw_func(arr, ["green" if x == i else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: write_final(i + 1))
        else:
            draw_func(arr, ["green"] * len(arr))

    count_step()


# Non-visual algorithm, used for complexity analysis (complexity_window)
def counting_sort_estudio(values):
    steps = 0

    if len(values) == 0:
        return steps

    max_val = max(values)
    min_val = min(values)
    value_range = max_val - min_val + 1

    count = [0] * value_range
    output = [0] * len(values)

    for num in values:
        count[num - min_val] += 1
        steps += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]
        steps += 1

    for num in reversed(values):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
        steps += 2

    for i in range(len(values)):
        values[i] = output[i]
        steps += 1

    return steps