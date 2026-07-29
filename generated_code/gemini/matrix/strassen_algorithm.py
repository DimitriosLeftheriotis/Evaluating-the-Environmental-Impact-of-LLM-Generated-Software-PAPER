def add_matrix(A, B):
    """Helper function to add two square matrices."""
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def sub_matrix(A, B):
    """Helper function to subtract matrix B from matrix A."""
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def strassen_algorithm(A, B):
    """
    Multiplies two square n x n matrices A and B using Strassen's algorithm.
    Assumes n is a power of 2.
    """
    n = len(A)

    # Base case: 1x1 matrix
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    # Partitioning matrix A into 4 submatrices
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    # Partitioning matrix B into 4 submatrices
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # Calculating the 7 Strassen products recursively
    M1 = strassen_algorithm(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_algorithm(add_matrix(A21, A22), B11)
    M3 = strassen_algorithm(A11, sub_matrix(B12, B22))
    M4 = strassen_algorithm(A22, sub_matrix(B21, B11))
    M5 = strassen_algorithm(add_matrix(A11, A12), B22)
    M6 = strassen_algorithm(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_algorithm(sub_matrix(A12, A22), add_matrix(B21, B22))

    # Computing submatrices of the result matrix C
    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(add_matrix(sub_matrix(M1, M2), M3), M6)

    # Combining the 4 submatrices into a single n x n matrix C
    C = []
    for i in range(mid):
        C.append(C11[i] + C12[i])
    for i in range(mid):
        C.append(C21[i] + C22[i])

    return C