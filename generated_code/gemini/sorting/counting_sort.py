def counting_sort(arr):
    # Handle empty list case
    if not arr:
        return []
    
    # Find the range of elements in the input list
    min_val = min(arr)
    max_val = max(arr)
    range_of_elements = max_val - min_val + 1
    
    # Initialize count array and output array
    count = [0] * range_of_elements
    output = [0] * len(arr)
    
    # Store the count of each element
    for num in arr:
        count[num - min_val] += 1
        
    # Change count[i] so that count[i] contains actual
    # position of this element in output array
    for i in range(1, len(count)):
        count[i] += count[i - 1]
        
    # Build the output array (navigating backwards preserves stability)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
        
    return output