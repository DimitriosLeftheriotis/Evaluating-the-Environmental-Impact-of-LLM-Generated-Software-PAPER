def radix_sort(arr):
    # Handle empty or single-element lists
    if not arr:
        return []

    # Handle negative numbers by separating them from non-negative numbers
    negatives = [-x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    def counting_sort_by_digit(data, exp):
        """Helper function to perform counting sort on data based on the digit at 'exp' place."""
        n = len(data)
        output = [0] * n
        count = [0] * 10

        # Store count of occurrences of each digit
        for num in data:
            index = (num // exp) % 10
            count[index] += 1

        # Change count[i] so that count[i] now contains the actual
        # position of this digit in output[]
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build the output array (traverse backwards to maintain stability)
        for i in range(n - 1, -1, -1):
            index = (data[i] // exp) % 10
            output[count[index] - 1] = data[i]
            count[index] -= 1

        return output

    def sort_non_negatives(data):
        if not data:
            return []
        max_num = max(data)
        exp = 1
        sorted_data = list(data)
        
        # Process each digit position (ones, tens, hundreds, etc.)
        while max_num // exp > 0:
            sorted_data = counting_sort_by_digit(sorted_data, exp)
            exp *= 10
            
        return sorted_data

    # Sort positive and negative parts
    sorted_positives = sort_non_negatives(positives)
    
    # Negative values are inverted, sorted, and then reversed back
    sorted_negatives = [-x for x in reversed(sort_non_negatives(negatives))]

    # Combine sorted negatives and sorted positives
    return sorted_negatives + sorted_positives