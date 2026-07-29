def strassen_algorithm(A, B):
    n = len(A)

    # Base case: 1x1 matrix multiplication
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # Helper to add two matrices
    def add(X, Y):
        size = len(X)
        return [[X[i][j] + Y[i][j] for j in range(size)] for i in range(size)]

    # Helper to subtract two matrices
    def subtract(X, Y):
        size = len(X)
        return [[X[i][j] - Y[i][j] for j in range(size)] for i in range(size)]

    # Helper to split a matrix into 4 quadrants
    def split(M):
        size = len(M)
        half = size // 2
        top_left = [row[:half] for row in M[:half]]
        top_right = [row[half:] for row in M[:half]]
        bottom_left = [row[:half] for row in M[half:]]
        bottom_right = [row[half:] for row in M[half:]]
        return top_left, top_right, bottom_left, bottom_right

    # Helper to combine 4 quadrants into a single matrix
    def combine(C11, C12, C21, C22):
        half = len(C11)
        size = half * 2
        C = [[0] * size for _ in range(size)]
        for i in range(half):
            for j in range(half):
                C[i][j] = C11[i][j]
                C[i][j + half] = C12[i][j]
                C[i + half][j] = C21[i][j]
                C[i + half][j + half] = C22[i][j]
        return C

    # Split A and B into quadrants
    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    # 7 Strassen products
    M1 = strassen_algorithm(add(A11, A22), add(B11, B22))
    M2 = strassen_algorithm(add(A21, A22), B11)
    M3 = strassen_algorithm(A11, subtract(B12, B22))
    M4 = strassen_algorithm(A22, subtract(B21, B11))
    M5 = strassen_algorithm(add(A11, A12), B22)
    M6 = strassen_algorithm(subtract(A21, A11), add(B11, B12))
    M7 = strassen_algorithm(subtract(A12, A22), add(B21, B22))

    # Combine results into the four quadrants of C
    C11 = add(subtract(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(subtract(add(M1, M3), M2), M6)

    # Combine quadrants into the full result matrix
    C = combine(C11, C12, C21, C22)

    return C