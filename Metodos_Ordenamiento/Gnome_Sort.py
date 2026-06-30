# Gnome Sort algorithm with animated visualization for the charting tool.
def gnome_sort(arr, draw_func, delay):

    state = draw_func.state
    n = len(arr)
    index = 0

    def step():
        nonlocal index

        if state["valor"] == "detenido":
            return
        if state["valor"] == "pausado":
            draw_func.canvas.after(100, step)
            return

        if index < n:
            if index == 0:
                index += 1
            elif arr[index] >= arr[index - 1]:
                index += 1
            else:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                colors = ["orange" if x == index or x == index - 1 else "gray" for x in range(n)]
                draw_func(arr, colors)
                index = max(0, index - 1)
                draw_func.canvas.after(int(delay * 100), step)
                return

            colors = ["green" if x < index else "gray" for x in range(n)]
            draw_func(arr, colors)
            draw_func.canvas.after(int(delay * 100), step)
        else:
            draw_func(arr, ["green"] * n)

    step()

# Non-visual Gnome Sort algorithm used for complexity analysis.
def gnome_sort_estudio(values):

    steps = 0
    n = len(values)
    index = 0

    while index < n:
        if index == 0:
            index += 1
            steps += 1
        elif values[index] >= values[index - 1]:
            steps += 1
            index += 1
        else:
            values[index], values[index - 1] = values[index - 1], values[index]
            steps += 2
            index = max(0, index - 1)

    return steps