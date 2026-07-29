def fibonacci_memoized(n, memo=None):
    if memo is None:
        memo = {}
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n in (0, 1):
        return n
    if n in memo:
        return memo[n]
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    return memo[n]