def lu_decomposition(matrix):
    n = len(matrix)

    # Initialize L and U matrices
    L = [[0.0 for _ in range(n)] for _ in range(n)]
    U = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        # Compute upper triangular matrix U
        for k in range(i, n):
            sum_upper = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matrix[i][k] - sum_upper

        # Compute lower triangular matrix L
        L[i][i] = 1.0
        for k in range(i + 1, n):
            sum_lower = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = (matrix[k][i] - sum_lower) / U[i][i]

    return L, U