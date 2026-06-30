# Animated algorithm (used by the visualization/chart window)
def bubble_sort(arr, draw_func, delay):
    n = len(arr)
    state = draw_func.state

    def step(i, j):
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, lambda: step(i, j))
            return

        if i < n - 1:
            if j < n - i - 1:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

                draw_func(arr, ["red" if x == j or x == j + 1 else "gray" for x in range(len(arr))])

                try:
                    draw_func.canvas.after(int(delay * 100), lambda: step(i, j + 1))
                except Exception as error:
                    print("Animation interrupted:", error)
            else:
                draw_func.canvas.after(1, lambda: step(i + 1, 0))

    step(0, 0)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def bubble_sort_estudio(values):
    steps = 0
    n = len(values)
    for i in range(n):
        for j in range(0, n - i - 1):
            steps += 1
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
                steps += 1
    return steps