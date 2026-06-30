# Animated algorithm (used by the visualization/chart window)
def cycle_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)

    def cycle(cycle_start):
        if cycle_start >= n - 1 or state["value"] == "stopped":
            draw_func(arr, ["green"] * n)
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: cycle(cycle_start))
            return

        item = arr[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            draw_func.canvas.after(1, lambda: cycle(cycle_start + 1))
            return

        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        draw_func(arr, ["orange" if x == pos else "gray" for x in range(n)])

        def resume_cycle(current_pos, current_item):
            if state["value"] == "stopped":
                return
            if state["value"] == "paused":
                draw_func.canvas.after(100, lambda: resume_cycle(current_pos, current_item))
                return

            new_pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < current_item:
                    new_pos += 1

            while current_item == arr[new_pos]:
                new_pos += 1

            if new_pos >= len(arr):
                draw_func.canvas.after(1, lambda: cycle(cycle_start + 1))
                return

            arr[new_pos], current_item = current_item, arr[new_pos]
            draw_func(arr, ["red" if x == new_pos else "gray" for x in range(n)])

            if new_pos != cycle_start:
                draw_func.canvas.after(int(delay * 100), lambda: resume_cycle(new_pos, current_item))
            else:
                draw_func.canvas.after(int(delay * 100), lambda: cycle(cycle_start + 1))

        draw_func.canvas.after(int(delay * 100), lambda: resume_cycle(pos, item))

    cycle(0)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def cycle_sort_estudio(values):
    steps = 0
    n = len(values)

    for cycle_start in range(n - 1):
        item = values[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, n):
            steps += 1
            if values[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == values[pos]:
            pos += 1
            steps += 1

        if pos < n:
            values[pos], item = item, values[pos]
            steps += 1

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                steps += 1
                if values[i] < item:
                    pos += 1

            while pos < n and item == values[pos]:
                pos += 1
                steps += 1

            if pos < n:
                values[pos], item = item, values[pos]
                steps += 1

    return steps