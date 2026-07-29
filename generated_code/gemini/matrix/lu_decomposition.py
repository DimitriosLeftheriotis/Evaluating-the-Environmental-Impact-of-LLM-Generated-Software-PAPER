def lu_decomposition(matrix):
    n = len(matrix)
    
    # Initialize L as an identity matrix (1s on diagonal, 0s elsewhere)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    # Initialize U as a zero matrix
    U = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        # Calculate upper triangular matrix U
        for k in range(i, n):
            sum_u = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = float(matrix[i][k] - sum_u)
            
        # Calculate lower triangular matrix L
        for k in range(i + 1, n):
            sum_l = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = float((matrix[k][i] - sum_l) / U[i][i])
            
    return L, U