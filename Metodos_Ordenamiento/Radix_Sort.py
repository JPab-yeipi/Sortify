# Animated algorithm (used by the visualization/chart window)
def radix_sort(arr, draw_func, delay):
    state = draw_func.state

    if len(arr) == 0:
        return

    max_num = max(arr)
    exp = 1

    def counting_sort_by_digit(exp, i=0, phase="counting", count=None, output=None):
        n = len(arr)
        if count is None:
            count = [0] * 10
            output = [0] * n

        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: counting_sort_by_digit(exp, i, phase, count, output))
            return

        if phase == "counting":
            if i < n:
                index = arr[i] // exp
                count[index % 10] += 1
                draw_func(arr, ["orange" if x == i else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: counting_sort_by_digit(exp, i + 1, "counting", count, output))
            else:
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, 1, "accumulating", count, output))

        elif phase == "accumulating":
            if i < 10:
                count[i] += count[i - 1]
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, i + 1, "accumulating", count, output))
            else:
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, n - 1, "sorting", count, output))

        elif phase == "sorting":
            if i >= 0:
                index = arr[i] // exp
                output[count[index % 10] - 1] = arr[i]
                count[index % 10] -= 1
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, i - 1, "sorting", count, output))
            else:
                draw_func.canvas.after(1, lambda: counting_sort_by_digit(exp, 0, "rewriting", count, output))

        elif phase == "rewriting":
            if i < n:
                arr[i] = output[i]
                draw_func(arr, ["blue" if x == i else "gray" for x in range(n)])
                draw_func.canvas.after(int(delay * 100), lambda: counting_sort_by_digit(exp, i + 1, "rewriting", count, output))
            else:
                next_exp(exp)

    def next_exp(current_exp):
        following = current_exp * 10
        if max_num // following > 0:
            counting_sort_by_digit(following)
        else:
            draw_func(arr, ["green"] * len(arr))

    counting_sort_by_digit(exp)


# Non-visual algorithm, used for complexity analysis (complexity_window)
def radix_sort_estudio(values):
    steps = 0
    if len(values) == 0:
        return steps

    max_num = max(values)
    exp = 1
    n = len(values)

    while max_num // exp > 0:
        count = [0] * 10
        output = [0] * n

        for i in range(n):
            index = values[i] // exp
            count[index % 10] += 1
            steps += 1

        for i in range(1, 10):
            count[i] += count[i - 1]
            steps += 1

        for i in range(n - 1, -1, -1):
            index = values[i] // exp
            output[count[index % 10] - 1] = values[i]
            count[index % 10] -= 1
            steps += 2

        for i in range(n):
            values[i] = output[i]
            steps += 1

        exp *= 10

    return steps