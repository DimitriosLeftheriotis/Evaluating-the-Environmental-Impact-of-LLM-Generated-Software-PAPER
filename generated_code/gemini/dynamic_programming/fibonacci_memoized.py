def fibonacci_memoized(n: int, memo: dict = None) -> int:
    """
    Calculates the n-th Fibonacci number using top-down dynamic programming (memoization).
    
    Parameters:
        n (int): A non-negative integer (0-indexed).
        memo (dict, optional): Dictionary used to cache calculated results.
        
    Returns:
        int: The n-th Fibonacci number.
    """
    # Initialize the memoization dictionary on the initial call
    if memo is None:
        memo = {}

    # Check if the result is already in the cache
    if n in memo:
        return memo[n]

    # Base cases
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Recursively calculate and store the result in the cache
    memo[n] = fibonacci_memoized(n - 1, memo) + fibonacci_memoized(n - 2, memo)
    
    return memo[n]