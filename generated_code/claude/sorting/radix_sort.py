def radix_sort(arr):
    if not arr:
        return []

    # Radix sort works on non-negative integers; separate negatives if present
    negatives = [-x for x in arr if x < 0]
    non_negatives = [x for x in arr if x >= 0]

    def _radix_sort_non_negative(nums):
        if not nums:
            return []
        max_val = max(nums)
        result = list(nums)
        exp = 1
        while max_val // exp > 0:
            result = _counting_sort_by_digit(result, exp)
            exp *= 10
        return result

    def _counting_sort_by_digit(nums, exp):
        n = len(nums)
        output = [0] * n
        count = [0] * 10

        for num in nums:
            digit = (num // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            digit = (nums[i] // exp) % 10
            output[count[digit] - 1] = nums[i]
            count[digit] -= 1

        return output

    sorted_non_negatives = _radix_sort_non_negative(non_negatives)
    sorted_negatives = _radix_sort_non_negative(negatives)
    sorted_negatives = [-x for x in reversed(sorted_negatives)]

    return sorted_negatives + sorted_non_negatives