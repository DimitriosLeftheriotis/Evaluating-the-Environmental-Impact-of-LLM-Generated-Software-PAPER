def matrix_determinant(matrix):
    """
    Compute the determinant of a square matrix using Euclidean division-based
    row reduction (Bareiss-like integer-preserving elimination).

    The algorithm avoids fraction arithmetic by using exact division steps.
    """
    n = len(matrix)

    if n == 0:
        return 1

    # Make a copy so the input matrix is not modified
    a = [row[:] for row in matrix]

    sign = 1
    previous_pivot = 1

    for k in range(n - 1):
        # Find a non-zero pivot if the current one is zero
        if a[k][k] == 0:
            swap_row = None
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    swap_row = i
                    break

            if swap_row is None:
                return 0

            a[k], a[swap_row] = a[swap_row], a[k]
            sign *= -1

        pivot = a[k][k]

        # Euclidean division-based elimination
        for i in range(k + 1, n):
            quotient = a[i][k] // pivot
            remainder = a[i][k] % pivot

            # Use the quotient to eliminate the leading entry.
            # The remainder handling keeps operations integer-only.
            if remainder != 0:
                quotient = (a[i][k] - remainder) // pivot

            for j in range(k, n):
                a[i][j] -= quotient * a[k][j]

            # If a remainder remains, perform a row operation that swaps
            # the smaller remainder into the pivot position (Euclidean step).
            if a[i][k] != 0:
                a[k], a[i] = a[i], a[k]
                sign *= -1
                pivot = a[k][k]

                for j in range(k, n):
                    quotient = a[i][j] // pivot
                    a[i][j] -= quotient * a[k][j]

        # Normalize the submatrix using the previous pivot (Bareiss step)
        if k > 0:
            for i in range(k + 1, n):
                for j in range(k + 1, n):
                    a[i][j] //= previous_pivot

        previous_pivot = a[k][k]

    return sign * a[n - 1][n - 1]