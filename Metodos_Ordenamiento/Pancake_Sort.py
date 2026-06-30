# Animated algorithm (used by the visualization/chart window)
def pancake_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)

    def flip(end):
        start = 0
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    def step(i):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: step(i))
            return

        if i > 1:
            max_idx = 0
            for j in range(1, i):
                if arr[j] > arr[max_idx]:
                    max_idx = j

            if max_idx != i - 1:
                flip(max_idx)
                draw_func(arr, ["red" if x <= max_idx else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: flip_and_continue(i))
            else:
                draw_func.canvas.after(1, lambda: step(i - 1))
        else:
            draw_func(arr, ["green"] * n)

    def flip_and_continue(i):
        flip(i - 1)
        draw_func(arr, ["blue" if x < i else "gray" for x in range(n)])
        draw_func.canvas.after(int(delay * 100), lambda: step(i - 1))

    step(n)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def pancake_sort_estudio(values):
    steps = 0

    def flip(end):
        nonlocal steps
        start = 0
        while start < end:
            values[start], values[end] = values[end], values[start]
            steps += 1
            start += 1
            end -= 1

    n = len(values)
    for i in range(n, 1, -1):
        max_idx = 0
        for j in range(1, i):
            steps += 1
            if values[j] > values[max_idx]:
                max_idx = j

        if max_idx != i - 1:
            flip(max_idx)
            flip(i - 1)

    return steps