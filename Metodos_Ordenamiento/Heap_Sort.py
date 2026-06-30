# Animated algorithm (used by the visualization/chart window)
def heap_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)
    build_index = n // 2 - 1
    extract_index = n - 1

    def heapify(n, i, callback):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: heapify(n, i, callback))
            return

        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            draw_func(arr, ["red" if x == i or x == largest else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: heapify(n, largest, callback))
        else:
            draw_func.canvas.after(1, callback)

    def build_heap():
        nonlocal build_index
        if build_index >= 0:
            heapify(n, build_index, lambda: build_heap_step())
        else:
            extract()

    def build_heap_step():
        nonlocal build_index
        build_index -= 1
        draw_func.canvas.after(1, build_heap)

    def extract():
        nonlocal extract_index
        if extract_index > 0:
            arr[extract_index], arr[0] = arr[0], arr[extract_index]
            draw_func(arr, ["green" if x >= extract_index else "gray" for x in range(len(arr))])
            draw_func.canvas.after(int(delay * 100), lambda: heapify(extract_index, 0, lambda: extract_step()))
        else:
            draw_func(arr, ["green"] * n)

    def extract_step():
        nonlocal extract_index
        extract_index -= 1
        draw_func.canvas.after(1, extract)

    build_heap()


# Non-visual algorithm, used for complexity analysis (complexity_window)
def heap_sort_estudio(values):
    steps = 0

    def heapify(n, i):
        nonlocal steps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Compare with left child
        if left < n:
            steps += 1  # index comparison
            steps += 1  # value comparison
            if values[left] > values[largest]:
                largest = left
        else:
            steps += 1  # failed index comparison

        # Compare with right child
        if right < n:
            steps += 1
            steps += 1
            if values[right] > values[largest]:
                largest = right
        else:
            steps += 1

        # Swap if needed
        if largest != i:
            values[i], values[largest] = values[largest], values[i]
            steps += 1  # swap
            heapify(n, largest)  # recursive call

    n = len(values)

    # Build the heap
    for i in range(n // 2 - 1, -1, -1):
        steps += 1  # control step
        heapify(n, i)

    # Extract the max and re-heapify
    for i in range(n - 1, 0, -1):
        values[i], values[0] = values[0], values[i]
        steps += 1  # swap
        heapify(i, 0)

    return steps