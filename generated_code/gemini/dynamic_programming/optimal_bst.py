def optimal_bst(keys, p, q, n):
    """
    Computes the minimum expected cost of an optimal binary search tree.
    
    Parameters:
    - keys: list of n sorted keys
    - p: list of probabilities for successful searches (length n, 1-indexed conceptually)
    - q: list of probabilities for unsuccessful searches (length n+1)
    - n: number of keys (int)
    
    Returns:
    - Minimum search cost (float or int)
    """
    # e[i][j] stores the expected cost of searching an optimal BST 
    # containing keys k_i through k_j
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    
    # w[i][j] stores the sum of probabilities for keys k_i..k_j and dummy keys d_(i-1)..d_j
    w = [[0.0] * (n + 1) for _ in range(n + 2)]

    # Base cases: subtrees with no keys (only a dummy key)
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    # l is the chain length (number of keys in subtree)
    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            e[i][j] = float('inf')
            # Update sum of probabilities
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]

            # Try each key k_r as the root of the subtree containing keys k_i..k_j
            for r in range(i, j + 1):
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j]:
                    e[i][j] = cost

    return e[1][n]