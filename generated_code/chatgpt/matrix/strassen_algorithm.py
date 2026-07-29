def strassen_algorithm(A, B):
    n = len(A)

    def add_matrix(X, Y):
        return [
            [X[i][j] + Y[i][j] for j in range(len(X))]
            for i in range(len(X))
        ]

    def sub_matrix(X, Y):
        return [
            [X[i][j] - Y[i][j] for j in range(len(X))]
            for i in range(len(X))
        ]

    def split_matrix(X):
        mid = len(X) // 2
        return (
            [row[:mid] for row in X[:mid]],       # Top-left
            [row[mid:] for row in X[:mid]],       # Top-right
            [row[:mid] for row in X[mid:]],       # Bottom-left
            [row[mid:] for row in X[mid:]]        # Bottom-right
        )

    def combine_matrix(C11, C12, C21, C22):
        top = [
            C11[i] + C12[i]
            for i in range(len(C11))
        ]
        bottom = [
            C21[i] + C22[i]
            for i in range(len(C21))
        ]
        return top + bottom

    def multiply(X, Y):
        size = len(X)

        if size == 1:
            return [[X[0][0] * Y[0][0]]]

        A11, A12, A21, A22 = split_matrix(X)
        B11, B12, B21, B22 = split_matrix(Y)

        # Seven Strassen multiplications
        M1 = multiply(add_matrix(A11, A22), add_matrix(B11, B22))
        M2 = multiply(add_matrix(A21, A22), B11)
        M3 = multiply(A11, sub_matrix(B12, B22))
        M4 = multiply(A22, sub_matrix(B21, B11))
        M5 = multiply(add_matrix(A11, A12), B22)
        M6 = multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
        M7 = multiply(sub_matrix(A12, A22), add_matrix(B21, B22))

        C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
        C12 = add_matrix(M3, M5)
        C21 = add_matrix(M2, M4)
        C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

        return combine_matrix(C11, C12, C21, C22)

    return multiply(A, B)