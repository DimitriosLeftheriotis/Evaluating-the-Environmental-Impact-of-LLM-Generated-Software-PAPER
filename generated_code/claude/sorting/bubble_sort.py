def bubble_sort(array):
    # Create a shallow copy to return a new list
    new_arr = list(array)
    n = len(new_arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if new_arr[j] > new_arr[j + 1]:
                new_arr[j], new_arr[j + 1] = new_arr[j + 1], new_arr[j]
                swapped = True
        if not swapped:
            break

    return new_arr
