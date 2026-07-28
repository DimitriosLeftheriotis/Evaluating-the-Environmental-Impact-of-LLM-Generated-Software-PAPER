def counting_sort(arr):
    if not arr:
        return []

    min_val = min(arr)
    max_val = max(arr)

    count = [0] * (max_val - min_val + 1)

    for num in arr:
        count[num - min_val] += 1

    result = []

    for i, freq in enumerate(count):
        result.extend([i + min_val] * freq)

    return result