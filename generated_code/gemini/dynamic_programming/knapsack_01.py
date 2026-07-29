def knapsack_01(weights: list[int], values: list[int], W: int) -> int:
    n = len(weights)
    
    # Initialize a 2D DP table with dimensions (n + 1) x (W + 1)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    # Build table dp[][] in bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            # Current item's weight and value (0-indexed adjustment)
            weight = weights[i - 1]
            value = values[i - 1]
            
            if weight <= w:
                # Max of including the item vs. excluding the item
                dp[i][w] = max(value + dp[i - 1][w - weight], dp[i - 1][w])
            else:
                # Weight exceeds capacity, exclude the item
                dp[i][w] = dp[i - 1][w]
                
    return dp[n][W]