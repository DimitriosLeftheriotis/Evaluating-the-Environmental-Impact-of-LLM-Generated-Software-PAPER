def fibonacci_memoized(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    memo = {0: 0, 1: 1}

    def helper(k):
        if k not in memo:
            memo[k] = helper(k - 1) + helper(k - 2)
        return memo[k]

    return helper(n)