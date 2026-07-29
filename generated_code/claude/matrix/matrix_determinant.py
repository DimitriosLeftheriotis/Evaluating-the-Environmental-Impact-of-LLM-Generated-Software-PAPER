def matrix_determinant(matrix):
    """
    Compute the determinant of a square matrix using Euclidean
    division-based row reduction (a fraction-free variant of Gaussian
    elimination inspired by the Euclidean algorithm for GCDs).

    Instead of using division to create a "1" pivot (which introduces
    fractions), this method repeatedly applies integer row combinations
    between the pivot row and the row being eliminated -- exactly like
    running the Euclidean algorithm on the pivot entry and the entry
    below it -- until the entry below the pivot becomes zero. Row swaps
    (which flip the sign of the determinant) are used whenever the
    remainder ends up smaller in the row that should become the pivot.

    Args:
        matrix: A square 2D list of numbers (ints or floats).

    Returns:
        The determinant of the matrix (int if all inputs are ints and
        no swaps introduce floats, otherwise a numeric value).

    Raises:
        ValueError: If the matrix is not square or is empty in an
                    inconsistent way (ragged rows).
    """
    n = len(matrix)

    # Validate square matrix
    for row in matrix:
        if len(row) != n:
            raise ValueError("Input matrix must be square (n x n).")

    if n == 0:
        return 1  # determinant of an empty matrix is conventionally 1

    # Work on a deep copy so the original matrix is not mutated
    mat = [row[:] for row in matrix]

    sign = 1

    for col in range(n):
        # Eliminate entries below the pivot in this column using
        # Euclidean-style row reduction (no division that produces
        # fractions -- only integer floor division to compute
        # quotients for row subtraction).
        for row in range(col + 1, n):
            # Keep reducing mat[row][col] against mat[col][col] the
            # way the Euclidean algorithm reduces two numbers, via
            # row operations R_row -> R_row - q * R_col.
            while mat[row][col] != 0:
                if mat[col][col] == 0:
                    # Pivot is zero but the row below has a nonzero
                    # entry: swap them so elimination can proceed.
                    mat[col], mat[row] = mat[row], mat[col]
                    sign = -sign
                    continue

                q = mat[row][col] // mat[col][col]
                for k in range(col, n):
                    mat[row][k] -= q * mat[col][k]

                if mat[row][col] != 0:
                    # The remainder ended up in the row below; swap
                    # so the (generally smaller) remainder becomes
                    # the new pivot candidate, mimicking Euclid's
                    # algorithm swapping (a, b) -> (b, a % b).
                    mat[col], mat[row] = mat[row], mat[col]
                    sign = -sign

        # If the pivot column is entirely zero from this row down,
        # the matrix is singular.
        if mat[col][col] == 0:
            return 0

    # After elimination, the matrix is upper triangular; the
    # determinant is the product of the diagonal, adjusted by the
    # accumulated sign from row swaps.
    det = sign
    for i in range(n):
        det *= mat[i][i]

    return det