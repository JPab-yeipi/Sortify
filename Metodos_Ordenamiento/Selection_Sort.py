# Animated algorithm (used by the visualization/chart window)
def selection_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)
    i = 0

    def outer_step():
        nonlocal i
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, outer_step)
            return
        if i >= n:
            draw_func(arr, ["green"] * n)
            return

        min_idx = i
        j = i + 1

        def find_minimum():
            nonlocal j, min_idx, i
            if state["value"] == "stopped":
                return
            if state["value"] == "paused":
                draw_func.canvas.after(100, find_minimum)
                return

            if j < n:
                if arr[j] < arr[min_idx]:
                    min_idx = j
                draw_func(arr, [
                    "red" if x == j else
                    "yellow" if x == min_idx else
                    "green" if x < i else "gray" for x in range(n)
                ])
                j += 1
                draw_func.canvas.after(int(delay * 100), find_minimum)
            else:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                draw_func(arr, ["green" if x <= i else "gray" for x in range(n)])
                i += 1
                draw_func.canvas.after(int(delay * 100), outer_step)

        find_minimum()

    outer_step()


# Non-visual algorithm, used for complexity analysis (complexity_window)
def selection_sort_estudio(values):
    steps = 0
    n = len(values)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps += 1
            if values[j] < values[min_idx]:
                min_idx = j
        values[i], values[min_idx] = values[min_idx], values[i]
        steps += 1
    return steps