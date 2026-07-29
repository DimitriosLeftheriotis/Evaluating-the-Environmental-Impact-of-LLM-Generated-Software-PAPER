def optimal_bst(keys, p, q, n):
    """
    Compute the minimum search cost of an Optimal Binary Search Tree.

    Parameters:
        keys: List of sorted keys (ascending order).
        p: List of search probabilities for the keys (1-indexed conceptually).
        q: List of dummy search probabilities for values outside key range.
        n: Number of keys.

    Returns:
        Minimum expected search cost of the optimal BST.
    """
    # e[i][j] stores the optimal cost of keys i through j
    e = [[0.0] * (n + 2) for _ in range(n + 2)]
    
    # w[i][j] stores the sum of probabilities from keys i through j
    # and dummy keys i-1 through j
    w = [[0.0] * (n + 2) for _ in range(n + 2)]

    # Base cases: empty subtrees
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    # Compute weights
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            w[i][j] = (
                w[i][j - 1] + p[j - 1] + q[j]
            )

            e[i][j] = float("inf")

            # Try each key as root
            for r in range(i, j + 1):
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j]:
                    e[i][j] = cost

    return e[1][n]