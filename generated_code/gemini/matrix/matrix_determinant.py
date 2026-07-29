def matrix_determinant(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    if any(len(row) != n for row in matrix):
        raise ValueError("Matrix must be square.")

    # Create a deep copy of the matrix to avoid modifying the input
    A = [row[:] for row in matrix]
    
    det_sign = 1

    for col in range(n):
        # Euclidean division-based elimination for the current column
        while True:
            # Find the row with the minimum non-zero absolute value in column `col` at or below `col`
            pivot_row = -1
            min_val = float('inf')
            
            for row in range(col, n):
                val = abs(A[row][col])
                if val != 0 and val < min_val:
                    min_val = val
                    pivot_row = row

            # If all elements in column `col` below the diagonal are zero
            if pivot_row == -1:
                return 0

            # Swap the current column's diagonal row with the chosen pivot row
            if pivot_row != col:
                A[col], A[pivot_row] = A[pivot_row], A[col]
                det_sign *= -1

            # Check if all elements below the pivot are zero
            all_zero_below = True
            for row in range(col + 1, n):
                if A[row][col] != 0:
                    all_zero_below = False
                    # Reduce A[row] using Euclidean division on A[col]
                    quotient = A[row][col] // A[col][col]
                    for c in range(col, n):
                        A[row][c] -= quotient * A[col][c]

            if all_zero_below:
                break

    # Calculate final determinant as product of diagonal elements adjusted by row-swap sign flips
    det = det_sign
    for i in range(n):
        det *= A[i][i]

    return det