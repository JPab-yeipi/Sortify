# Animated algorithm (used by the visualization/chart window)
def insertion_sort(arr, draw_func, delay):
    state = draw_func.state

    def step(i):
        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, lambda: step(i))
            return

        if i < len(arr):
            key = arr[i]
            j = i - 1

            def move(j_inner):
                if state["value"] == "stopped":
                    return
                elif state["value"] == "paused":
                    draw_func.canvas.after(100, lambda: move(j_inner))
                    return

                if j_inner >= 0 and arr[j_inner] > key:
                    arr[j_inner + 1] = arr[j_inner]
                    draw_func(arr, ["orange" if x == j_inner or x == i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: move(j_inner - 1))
                else:
                    arr[j_inner + 1] = key
                    draw_func(arr, ["green" if x <= i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: step(i + 1))

            move(j)
        else:
            draw_func(arr, ["green"] * len(arr))

    step(1)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def insertion_sort_estudio(values):
    steps = 0
    for i in range(1, len(values)):
        key = values[i]
        j = i - 1

        while j >= 0:
            steps += 1
            if values[j] > key:
                values[j + 1] = values[j]
                steps += 1
                j -= 1
            else:
                break

        values[j + 1] = key
        steps += 1

    return steps