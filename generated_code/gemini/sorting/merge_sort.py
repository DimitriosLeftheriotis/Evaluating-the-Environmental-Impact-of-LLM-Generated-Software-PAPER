def merge_sort(arr: list[int]) -> list[int]:
    """Sorts a list of integers in ascending order using the Merge Sort algorithm.
    
    Returns a new sorted list without modifying the original input.
    """
    # Base case: lists with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr[:]
    
    # Divide: Find the midpoint and split the array into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # Conquer: Merge the sorted halves
    return _merge(left_half, right_half)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Helper function to merge two sorted lists into a single sorted list."""
    merged = []
    i = j = 0
    
    # Compare elements from both lists and append the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged