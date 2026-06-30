# Animated algorithm (used by the visualization/chart window)
def merge_sort(arr, draw_func, delay):
    state = draw_func.state

    def merge_sort_recursive(start, end, callback):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: merge_sort_recursive(start, end, callback))
            return

        if start < end:
            mid = (start + end) // 2
            merge_sort_recursive(start, mid, lambda: merge_sort_recursive(mid + 1, end, lambda: merge(start, mid, end, callback)))
        else:
            draw_func.canvas.after(1, callback)

    def merge(start, mid, end, callback):
        if state["value"] == "stopped":
            return
        if state["value"] == "paused":
            draw_func.canvas.after(100, lambda: merge(start, mid, end, callback))
            return

        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]
        i = j = 0
        k = start

        def merge_step():
            nonlocal i, j, k
            if state["value"] == "stopped":
                return
            if state["value"] == "paused":
                draw_func.canvas.after(100, merge_step)
                return

            if i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                draw_func(arr, ["purple" if x == k else "gray" for x in range(len(arr))])
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            elif i < len(left):
                arr[k] = left[i]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(len(arr))])
                i += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            elif j < len(right):
                arr[k] = right[j]
                draw_func(arr, ["purple" if x == k else "gray" for x in range(len(arr))])
                j += 1
                k += 1
                draw_func.canvas.after(int(delay * 100), merge_step)
            else:
                draw_func.canvas.after(1, callback)

        merge_step()

    merge_sort_recursive(0, len(arr) - 1, lambda: draw_func(arr, ["green"] * len(arr)))


# Non-visual algorithm, used for complexity analysis (complexity_window)
def merge_sort_estudio(values):
    steps = 0

    def merge(left, right):
        nonlocal steps
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            steps += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            steps += 1

        result.extend(left[i:])
        result.extend(right[j:])
        steps += len(left[i:]) + len(right[j:])
        return result

    def merge_sort_recursive(sub_array):
        if len(sub_array) <= 1:
            return sub_array

        mid = len(sub_array) // 2
        left = merge_sort_recursive(sub_array[:mid])
        right = merge_sort_recursive(sub_array[mid:])
        return merge(left, right)

    result = merge_sort_recursive(values)
    for i in range(len(values)):
        values[i] = result[i]
        steps += 1

    return steps