def heap_sort(arr: list[int]) -> list[int]:
    """Sorts a list of integers in ascending order using Heap Sort.
    
    Returns a new sorted list, leaving the original list unmodified.
    """
    # Work on a copy to avoid mutating the original input list
    data = arr.copy()
    n = len(data)

    def heapify(length: int, i: int) -> None:
        """Helper to maintain the max-heap property for a subtree rooted at index i."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Check if left child exists and is greater than root
        if left < length and data[left] > data[largest]:
            largest = left

        # Check if right child exists and is greater than current largest
        if right < length and data[right] > data[largest]:
            largest = right

        # If largest is not root, swap and continue heapifying the affected subtree
        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            heapify(length, largest)

    # Step 1: Build a max-heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # Step 2: Extract elements one by one from the heap
    for i in range(n - 1, 0, -1):
        # Move current root (largest element) to the end
        data[0], data[i] = data[i], data[0]
        
        # Call heapify on the reduced heap
        heapify(i, 0)

    return data