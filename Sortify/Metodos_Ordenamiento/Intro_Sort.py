# Animated algorithm (used by the visualization/chart window)
def intro_sort(arr, draw_func, delay):
    import math
    state = draw_func.state
    n = len(arr)

    def insertion_sort(start, end, callback):
        def step(i):
            if i > end:
                callback()
                return
            key = arr[i]
            j = i - 1

            def move(j_inner):
                if state["value"] == "stopped":
                    return
                if state["value"] == "paused":
                    draw_func.canvas.after(100, lambda: move(j_inner))
                    return

                if j_inner >= start and arr[j_inner] > key:
                    arr[j_inner + 1] = arr[j_inner]
                    draw_func(arr, ["orange" if x == j_inner or x == i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: move(j_inner - 1))
                else:
                    arr[j_inner + 1] = key
                    draw_func(arr, ["green" if x <= i else "gray" for x in range(len(arr))])
                    draw_func.canvas.after(int(delay * 100), lambda: step(i + 1))

            move(j)

        step(start + 1)

    def heapify(n, i, offset, callback):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: heapify(n, i, offset, callback))
            return

        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[offset + l] > arr[offset + largest]:
            largest = l
        if r < n and arr[offset + r] > arr[offset + largest]:
            largest = r

        if largest != i:
            arr[offset + i], arr[offset + largest] = arr[offset + largest], arr[offset + i]
            draw_func(arr, ["red" if x == offset + i or x == offset + largest else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: heapify(n, largest, offset, callback))
        else:
            draw_func.canvas.after(1, callback)

    def heap_sort(start, end, callback):
        n = end - start + 1
        i_build = n // 2 - 1
        i_extract = n - 1

        def build():
            nonlocal i_build
            if i_build >= 0:
                heapify(n, i_build, start, lambda: step_build())
            else:
                extract()

        def step_build():
            nonlocal i_build
            i_build -= 1
            draw_func.canvas.after(1, build)

        def extract():
            nonlocal i_extract
            if i_extract > 0:
                arr[start + i_extract], arr[start] = arr[start], arr[start + i_extract]
                draw_func(arr, ["blue" if x == start + i_extract else "gray" for x in range(len(arr))])
                draw_func.canvas.after(int(delay * 100), lambda: heapify(i_extract, 0, start, step_extract))
            else:
                callback()

        def step_extract():
            nonlocal i_extract
            i_extract -= 1
            draw_func.canvas.after(1, extract)

        build()

    def quick_sort(start, end, depth_limit, callback):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: quick_sort(start, end, depth_limit, callback))
            return

        size = end - start + 1
        if size <= 16:
            insertion_sort(start, end, callback)
            return
        if depth_limit == 0:
            heap_sort(start, end, callback)
            return

        pivot = arr[end]
        i = start - 1
        j = start

        def partition_step():
            nonlocal i, j
            if j < end:
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    draw_func(arr, ["red" if x == i or x == j else "gray" for x in range(len(arr))])
                j += 1
                draw_func.canvas.after(int(delay * 100), partition_step)
            else:
                arr[i + 1], arr[end] = arr[end], arr[i + 1]
                p = i + 1
                quick_sort(start, p - 1, depth_limit - 1, lambda: quick_sort(p + 1, end, depth_limit - 1, callback))

        partition_step()

    depth_limit = 2 * math.floor(math.log2(len(arr))) if len(arr) > 0 else 0

    quick_sort(0, len(arr) - 1, depth_limit, lambda: draw_func(arr, ["green"] * len(arr)))


# Non-visual algorithm, used for complexity analysis (complexity_window)
def intro_sort_estudio(values):
    import math
    steps = 0

    def insertion_sort(start, end):
        nonlocal steps
        for i in range(start + 1, end + 1):
            key = values[i]
            j = i - 1
            while j >= start and values[j] > key:
                steps += 1
                values[j + 1] = values[j]
                steps += 1
                j -= 1
            values[j + 1] = key
            steps += 1

    def heapify(n, i, offset):
        nonlocal steps
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        steps += 1
        if l < n and values[offset + l] > values[offset + largest]:
            largest = l

        steps += 1
        if r < n and values[offset + r] > values[offset + largest]:
            largest = r

        if largest != i:
            values[offset + i], values[offset + largest] = values[offset + largest], values[offset + i]
            steps += 1
            heapify(n, largest, offset)

    def heap_sort(start, end):
        nonlocal steps
        n = end - start + 1
        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i, start)
        for i in range(n - 1, 0, -1):
            values[start + i], values[start] = values[start], values[start + i]
            steps += 1
            heapify(i, 0, start)

    def quick_sort(start, end, depth_limit):
        nonlocal steps
        size = end - start + 1
        if size <= 16:
            insertion_sort(start, end)
            return
        if depth_limit == 0:
            heap_sort(start, end)
            return

        pivot = values[end]
        i = start - 1
        for j in range(start, end):
            steps += 1
            if values[j] <= pivot:
                i += 1
                values[i], values[j] = values[j], values[i]
                steps += 1

        values[i + 1], values[end] = values[end], values[i + 1]
        steps += 1
        p = i + 1

        quick_sort(start, p - 1, depth_limit - 1)
        quick_sort(p + 1, end, depth_limit - 1)

    depth_limit = 2 * math.floor(math.log2(len(values))) if len(values) > 0 else 0
    quick_sort(0, len(values) - 1, depth_limit)

    return steps