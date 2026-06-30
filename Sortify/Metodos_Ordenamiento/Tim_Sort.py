# Tim Sort algorithm with animated visualization for the charting tool.
def tim_sort(arr, draw_func, delay):
    
    state = draw_func.state
    MIN_RUN = 32
    n = len(arr)

    def insertion_sort(start, end, callback):
        def step(i):
            if state["valor"] == "detenido":
                return
            if i > end:
                callback()
                return
            
            key = arr[i]
            j = i - 1

            def move(current_j):
                if state["valor"] == "detenido":
                    return
                if state["valor"] == "pausado":
                    draw_func.canvas.after(100, lambda: move(current_j))
                    return

                if current_j >= start and arr[current_j] > key:
                    arr[current_j + 1] = arr[current_j]
                    colors = ["orange" if x == current_j or x == i else "gray" for x in range(n)]
                    draw_func(arr, colors)
                    draw_func.canvas.after(int(delay * 100), lambda: move(current_j - 1))
                else:
                    arr[current_j + 1] = key
                    colors = ["green" if start <= x <= i else "gray" for x in range(n)]
                    draw_func(arr, colors)
                    draw_func.canvas.after(int(delay * 100), lambda: step(i + 1))

            move(j)

        step(start + 1)

    def merge(left, mid, right, callback):
        len1, len2 = mid - left + 1, right - mid
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        def merge_step():
            nonlocal i, j, k
            if state["valor"] == "detenido":
                return
            if state["valor"] == "pausado":
                draw_func.canvas.after(100, merge_step)
                return

            if i < len1 and j < len2:
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
                draw_func(arr, ["purple" if x == k else "gray" for x in range(n)])
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            elif i < len1:
                arr[k] = left_part[i]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(n)])
                i += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            elif j < len2:
                arr[k] = right_part[j]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(n)])
                j += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            else:
                callback()

        merge_step()

    def sort_blocks(start_idx):
        if start_idx >= n:
            merge_pass(MIN_RUN)
            return
        end_idx = min(start_idx + MIN_RUN - 1, n - 1)
        insertion_sort(start_idx, end_idx, lambda: sort_blocks(start_idx + MIN_RUN))

    def merge_pass(current_size):
        if current_size >= n:
            draw_func(arr, ["green"] * n)
            return

        merges = []
        for left in range(0, n, 2 * current_size):
            mid = min(n - 1, left + current_size - 1)
            right = min((left + 2 * current_size - 1), n - 1)
            if mid < right:
                merges.append((left, mid, right))

        def apply_merge(idx):
            if idx < len(merges):
                l, m, r = merges[idx]
                merge(l, m, r, lambda: apply_merge(idx + 1))
            else:
                merge_pass(current_size * 2)

        apply_merge(0)

    sort_blocks(0)

# Non-visual Tim Sort algorithm used for complexity analysis.
def tim_sort_estudio(values):
    
    steps = 0
    MIN_RUN = 32
    n = len(values)

    def insertion_sort(start, end):
        nonlocal steps
        for i in range(start + 1, end + 1):
            key = values[i]
            j = i - 1
            while j >= start and values[j] > key:
                values[j + 1] = values[j]
                j -= 1
                steps += 2
            values[j + 1] = key
            steps += 1

    def merge(left, mid, right):
        nonlocal steps
        left_part = values[left:mid + 1]
        right_part = values[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            steps += 1
            if left_part[i] <= right_part[j]:
                values[k] = left_part[i]
                i += 1
            else:
                values[k] = right_part[j]
                j += 1
            steps += 1
            k += 1

        while i < len(left_part):
            values[k] = left_part[i]
            i += 1
            k += 1
            steps += 1

        while j < len(right_part):
            values[k] = right_part[j]
            j += 1
            k += 1
            steps += 1

    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        insertion_sort(start, end)

    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), n - 1)
            if mid < right:
                merge(left, mid, right)
        size *= 2

    return steps