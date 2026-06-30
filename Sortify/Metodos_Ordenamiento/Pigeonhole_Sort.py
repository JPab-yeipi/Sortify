# Animated algorithm (used by the visualization/chart window)
def pigeonhole_sort(arr, draw_func, delay):
    state = draw_func.state

    if len(arr) == 0:
        return

    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    insert_index = 0
    total = len(arr)

    def distribute_step(step):
        if step >= total or state["value"] == "stopped":
            fill_step(0, 0)
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: distribute_step(step))
            return

        number = arr[step]
        holes[number - min_val].append(number)
        draw_func(arr, ["purple" if x == step else "gray" for x in range(len(arr))])
        draw_func.canvas.after(int(delay * 100), lambda: distribute_step(step + 1))

    def fill_step(h, idx):
        nonlocal insert_index
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: fill_step(h, idx))
            return

        if h < len(holes):
            if idx < len(holes[h]):
                arr[insert_index] = holes[h][idx]
                draw_func(arr, ["green" if x == insert_index else "gray" for x in range(len(arr))])
                insert_index += 1
                draw_func.canvas.after(int(delay * 100), lambda: fill_step(h, idx + 1))
            else:
                draw_func.canvas.after(1, lambda: fill_step(h + 1, 0))
        else:
            draw_func(arr, ["green"] * len(arr))

    distribute_step(0)

# Non-visual algorithm, used for complexity analysis (complexity_window)
def pigeonhole_sort_estudio(values):
    steps = 0

    if len(values) == 0:
        return steps

    min_val = min(values)
    max_val = max(values)
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]

    for number in values:
        holes[number - min_val].append(number)
        steps += 1

    i = 0
    for hole in holes:
        for number in hole:
            values[i] = number
            steps += 1
            i += 1

    return steps