def naive_matrix_multiplication(A, B):
    n = len(A)
    m = len(B)
    p = len(B[0]) if m > 0 else 0

    # Validate dimensions: number of columns in A must equal number of rows in B
    k = len(A[0]) if n > 0 else 0
    if k != m:
        raise ValueError("Number of columns in A must equal number of rows in B")

    C = [[0 for _ in range(p)] for _ in range(n)]

    for i in range(n):
        for j in range(p):
            total = 0
            for l in range(k):
                total += A[i][l] * B[l][j]
            C[i][j] = total

    return C