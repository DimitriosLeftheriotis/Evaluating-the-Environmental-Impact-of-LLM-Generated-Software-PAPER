def naive_matrix_multiplication(A, B):
    """
    Multiply two matrices using the naive (standard) matrix multiplication algorithm.

    Args:
        A: 2D list representing the first matrix.
        B: 2D list representing the second matrix.

    Returns:
        2D list representing the product matrix C.
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Matrix dimensions are not compatible for multiplication.")

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C