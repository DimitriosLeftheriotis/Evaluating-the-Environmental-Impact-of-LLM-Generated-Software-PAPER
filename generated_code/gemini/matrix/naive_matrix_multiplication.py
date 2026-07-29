def naive_matrix_multiplication(A, B):
    """
    Multiplies two 2D matrices A and B using the standard (naive) algorithm.
    
    :param A: 2D list representing an m x n matrix
    :param B: 2D list representing an n x p matrix
    :return: 2D list representing the resulting m x p matrix C
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Matrix multiplication requires the number of columns in A 
    # to equal the number of rows in B.
    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices: Inner dimensions must match.")

    # Initialize the result matrix C with dimensions rows_A x cols_B with zeros
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Standard triple nested loop
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C