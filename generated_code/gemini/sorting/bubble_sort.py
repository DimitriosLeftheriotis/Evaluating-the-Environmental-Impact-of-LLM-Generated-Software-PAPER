def bubble_sort(arr: list[int]) -> list[int]:
    """
    Sorts a list of integers in ascending order using the Bubble Sort algorithm.
    Returns a new sorted list without modifying the original input list.
    """
    # Create a copy of the input list to avoid mutating the original
    sorted_arr = list(arr)
    n = len(sorted_arr)
    
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if sorted_arr[j] > sorted_arr[j + 1]:
                # Swap elements
                sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
                swapped = True
                
        # If no two elements were swapped in the inner loop, the list is already sorted
        if not swapped:
            break
            
    return sorted_arr
