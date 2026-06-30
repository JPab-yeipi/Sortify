# Animated algorithm (used by the visualization/chart window)
def cocktail_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)
    start = 0
    end = n - 1
    direction = 1

    def step(i, start, end, direction, changed):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: step(i, start, end, direction, changed))
            return

        if direction == 1:
            if i < end:
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    changed = True
                draw_func(arr, ["red" if x == i or x == i + 1 else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: step(i + 1, start, end, direction, changed))
            else:
                if not changed:
                    draw_func(arr, ["green"] * n)
                    return
                end -= 1
                draw_func.canvas.after(1, lambda: step(end, start, end, -1, False))
        else:
            if i > start:
                if arr[i] < arr[i - 1]:
                    arr[i], arr[i - 1] = arr[i - 1], arr[i]
                    changed = True
                draw_func(arr, ["red" if x == i or x == i - 1 else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: step(i - 1, start, end, direction, changed))
            else:
                if not changed:
                    draw_func(arr, ["green"] * n)
                    return
                start += 1
                draw_func.canvas.after(1, lambda: step(start, start, end, 1, False))

    step(start, start, end, direction, False)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def cocktail_sort_estudio(values):
    steps = 0
    n = len(values)
    start = 0
    end = n - 1
    changed = True

    while changed:
        changed = False

        for i in range(start, end):
            steps += 1
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                steps += 1
                changed = True

        end -= 1

        for i in range(end, start, -1):
            steps += 1
            if values[i] < values[i - 1]:
                values[i], values[i - 1] = values[i - 1], values[i]
                steps += 1
                changed = True

        start += 1

    return steps