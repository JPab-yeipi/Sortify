# Bucket Sort algorithm with animated visualization for the charting tool.
def bucket_sort(arr, draw_func, delay):
    state = draw_func.state
    n = len(arr)

    if n == 0:
        return

    max_val = max(arr)
    bucket_range = max_val / n
    buckets = [[] for _ in range(n)]
    insertion_idx = 0

    def distribute_into_buckets(i):
        if state["valor"] == "detenido":
            return
        if state["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: distribute_into_buckets(i))
            return

        if i < n:
            num = arr[i]
            bucket_idx = int(num / bucket_range)
            
            if bucket_idx != n:
                buckets[bucket_idx].append(num)
            else:
                buckets[n - 1].append(num)

            colors = ["blue" if x == i else "gray" for x in range(n)]
            draw_func(arr, colors)
            draw_func.canvas.after(int(delay * 100), lambda: distribute_into_buckets(i + 1))
        else:
            sort_and_merge_buckets(0, 0)

    def sort_and_merge_buckets(bucket_idx, pos):
        if state["valor"] == "detenido":
            return
        if state["valor"] == "pausado":
            draw_func.canvas.after(100, lambda: sort_and_merge_buckets(bucket_idx, pos))
            return

        nonlocal insertion_idx

        if bucket_idx < len(buckets):
            sorted_bucket = sorted(buckets[bucket_idx])
            if pos < len(sorted_bucket):
                arr[insertion_idx] = sorted_bucket[pos]
                colors = ["green" if x == insertion_idx else "gray" for x in range(n)]
                draw_func(arr, colors)
                insertion_idx += 1
                draw_func.canvas.after(int(delay * 100), lambda: sort_and_merge_buckets(bucket_idx, pos + 1))
            else:
                draw_func.canvas.after(1, lambda: sort_and_merge_buckets(bucket_idx + 1, 0))
        else:
            draw_func(arr, ["green"] * n)

    distribute_into_buckets(0)


# Non-visual Bucket Sort algorithm used for complexity analysis.  
def bucket_sort_estudio(values):

    steps = 0
    n = len(values)

    if n == 0:
        return steps

    max_val = max(values)
    bucket_range = max_val / n
    buckets = [[] for _ in range(n)]

    for num in values:
        bucket_idx = int(num / bucket_range)
        if bucket_idx != n:
            buckets[bucket_idx].append(num)
        else:
            buckets[n - 1].append(num)
        steps += 1

    idx = 0
    for bucket in buckets:
        bucket.sort()
        for num in bucket:
            values[idx] = num
            steps += 1
            idx += 1

    return steps