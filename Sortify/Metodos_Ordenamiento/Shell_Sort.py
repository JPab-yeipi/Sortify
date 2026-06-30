# Animated algorithm (used by the visualization/chart window)
def shell_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2

    gap_index = 0
    i = 0
    j = 0
    temp = None
    phase = "start"

    def step():
        nonlocal gap_index, i, j, temp, phase

        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, step)
            return

        if gap_index >= len(gaps):
            draw_func(arr, ["green"] * n)
            return

        gap = gaps[gap_index]

        if phase == "start":
            if i >= n:
                gap_index += 1
                if gap_index < len(gaps):
                    gap = gaps[gap_index]
                    i = gap
                    phase = "start"
                    draw_func.canvas.after(1, step)
                else:
                    draw_func(arr, ["green"] * n)
                return
            temp = arr[i]
            j = i
            phase = "comparing"
            draw_func.canvas.after(1, step)

        elif phase == "comparing":
            if j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                draw_func(arr, ["orange" if x == j or x == j - gap else "gray" for x in range(n)])
                j -= gap
                draw_func.canvas.after(int(delay * 100), step)
            else:
                phase = "inserting"
                draw_func.canvas.after(1, step)

        elif phase == "inserting":
            arr[j] = temp
            draw_func(arr, ["green" if x == j else "gray" for x in range(n)])
            i += 1
            phase = "start"
            draw_func.canvas.after(int(delay * 100), step)

    i = gaps[0] if gaps else 0
    step()


# Non-visual algorithm, used for complexity analysis (complexity_window)
def shell_sort_estudio(values):
    steps = 0
    n = len(values)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            steps += 1

            temp = values[i]
            j = i

            while j >= gap:
                steps += 1
                if values[j - gap] > temp:
                    values[j] = values[j - gap]
                    steps += 1
                    j -= gap
                else:
                    break

            values[j] = temp
            steps += 1

        gap //= 2

    return steps