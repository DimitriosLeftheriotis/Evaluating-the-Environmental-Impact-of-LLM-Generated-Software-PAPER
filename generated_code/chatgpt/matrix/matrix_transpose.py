def matrix_transpose(matrix):
    if not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    transposed = [[None] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]

    return transposed