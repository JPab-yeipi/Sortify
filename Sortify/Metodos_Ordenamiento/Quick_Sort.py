# Animated algorithm (used by the visualization/chart window)
def quick_sort(arr, draw_func, delay):
    state = draw_func.state
    stack = [(0, len(arr) - 1)]

    def step():
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, step)
            return

        if not stack:
            draw_func(arr, ["green"] * len(arr))
            return

        low, high = stack.pop()

        if low < high:
            i = low - 1
            pivot = arr[high]
            j = low

            def partition_step():
                nonlocal i, j
                if state["value"] == "stopped":
                    return
                if state["value"] == "paused":
                    draw_func.canvas.after(100, partition_step)
                    return

                if j < high:
                    if arr[j] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        draw_func(arr, ["red" if x == i or x == j else "gray" for x in range(len(arr))])
                    j += 1
                    draw_func.canvas.after(int(delay * 100), partition_step)
                else:
                    arr[i + 1], arr[high] = arr[high], arr[i + 1]
                    draw_func(arr, ["blue" if x == i + 1 else "gray" for x in range(len(arr))])
                    stack.append((low, i))
                    stack.append((i + 2, high))
                    draw_func.canvas.after(int(delay * 100), step)

            partition_step()
        else:
            draw_func.canvas.after(1, step)

    step()


# Non-visual algorithm, used for complexity analysis (complexity_window)
def quick_sort_estudio(values):
    steps = 0

    def partition(low, high):
        nonlocal steps
        pivot = values[high]
        i = low - 1

        for j in range(low, high):
            steps += 1
            if values[j] <= pivot:
                i += 1
                values[i], values[j] = values[j], values[i]
                steps += 1

        values[i + 1], values[high] = values[high], values[i + 1]
        steps += 1
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(values) - 1)
    return steps