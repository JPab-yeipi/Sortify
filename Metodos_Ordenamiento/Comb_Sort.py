# Animated algorithm (used by the visualization/chart window)
def comb_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False

    def step():
        nonlocal gap, sorted_flag

        if state["value"] == "stopped":
            return
        elif state["value"] == "paused":
            draw_func.canvas.after(100, step)
            return

        if gap > 1:
            gap = int(gap / shrink)
        else:
            gap = 1
            sorted_flag = True

        i = 0

        def compare_step():
            nonlocal i, sorted_flag
            if state["value"] == "stopped":
                return
            elif state["value"] == "paused":
                draw_func.canvas.after(100, compare_step)
                return

            if i + gap < n:
                if arr[i] > arr[i + gap]:
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    sorted_flag = False

                draw_func(arr, ["red" if x == i or x == i + gap else "gray" for x in range(n)])
                i += 1
                draw_func.canvas.after(int(delay * 100), compare_step)
            else:
                if not sorted_flag or gap != 1:
                    draw_func.canvas.after(1, step)
                else:
                    draw_func(arr, ["green"] * n)

        compare_step()

    step()


# Non-visual algorithm, used for complexity analysis (complexity_window)
def comb_sort_estudio(values):
    steps = 0
    n = len(values)
    gap = n
    shrink = 1.3

    while True:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        else:
            sorted_flag = False

        i = 0
        while i + gap < n:
            steps += 1
            if values[i] > values[i + gap]:
                values[i], values[i + gap] = values[i + gap], values[i]
                steps += 2
                sorted_flag = False
            i += 1

        if gap == 1 and sorted_flag:
            break

    return steps