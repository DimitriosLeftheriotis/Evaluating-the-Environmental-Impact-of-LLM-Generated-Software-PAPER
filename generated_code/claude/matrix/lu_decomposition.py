def lu_decomposition(matrix):
    n = len(matrix)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        # Upper triangular
        for k in range(i, n):
            sum_upper = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = matrix[i][k] - sum_upper

        # Lower triangular
        for k in range(i, n):
            if i == k:
                L[i][i] = 1.0
            else:
                sum_lower = sum(L[k][j] * U[j][i] for j in range(i))
                L[k][i] = (matrix[k][i] - sum_lower) / U[i][i]

    return (L, U)