def matrix_transpose(matrix):
    """
    Transposes a 2D list (matrix) of size m x n into size n x m.
    
    :param matrix: List[List[Any]] - input 2D list
    :return: List[List[Any]] - transposed 2D list
    """
    if not matrix or not matrix[0]:
        return []

    # Get dimensions
    rows = len(matrix)
    cols = len(matrix[0])

    # Construct the transposed matrix
    transposed = []
    for c in range(cols):
        new_row = []
        for r in range(rows):
            new_row.append(matrix[r][c])
        transposed.append(new_row)

    return transposed