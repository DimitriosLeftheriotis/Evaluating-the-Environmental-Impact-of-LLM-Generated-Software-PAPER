def radix_sort(arr):
    """
    Sort a list of integers in ascending order using Radix Sort.

    Returns a new sorted list without modifying the input list.
    """
    if not arr:
        return []

    def counting_sort_by_digit(nums, exp):
        output = [0] * len(nums)
        count = [0] * 10

        for num in nums:
            digit = (num // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for num in reversed(nums):
            digit = (num // exp) % 10
            output[count[digit] - 1] = num
            count[digit] -= 1

        return output

    def radix_sort_non_negative(nums):
        if not nums:
            return []

        result = nums[:]
        max_num = max(result)
        exp = 1

        while max_num // exp > 0:
            result = counting_sort_by_digit(result, exp)
            exp *= 10

        return result

    positives = [x for x in arr if x >= 0]
    negatives = [-x for x in arr if x < 0]

    sorted_positives = radix_sort_non_negative(positives)
    sorted_negatives = radix_sort_non_negative(negatives)

    return [-x for x in reversed(sorted_negatives)] + sorted_positives