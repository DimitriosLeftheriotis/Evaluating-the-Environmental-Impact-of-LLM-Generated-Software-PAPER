def matrix_determinant(matrix):
    """
    Compute the determinant of a square matrix.

    - For matrices containing only exact types (int, and Fraction if
      present), uses fraction-free Euclidean division-based row
      reduction: no float arithmetic, no rounding, guaranteed
      termination because the integer remainder produced by each
      row-combination step strictly decreases in absolute value
      (exactly like the Euclidean GCD algorithm).
    - For matrices containing any float entries, exact "!= 0" zero
      checks and floor-division quotients are meaningless (floating
      point round-off almost never lands on exact 0.0), so this falls
      back to standard partial-pivoting Gaussian elimination with a
      numeric tolerance for zero. This avoids the infinite swap/loop
      failure that occurs when Euclidean-style logic is applied to
      floats.

    Args:
        matrix: A square 2D list of numbers (ints and/or floats).

    Returns:
        The determinant of the matrix (exact int for integer input,
        float for float input).

    Raises:
        ValueError: If the matrix is not square (ragged or non-square).
    """
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise ValueError("Input matrix must be square (n x n).")

    if n == 0:
        return 1

    has_float = any(isinstance(v, float) for row in matrix for v in row)

    if has_float:
        return _determinant_float_gaussian(matrix, n)
    else:
        return _determinant_exact_euclidean(matrix, n)


def _determinant_exact_euclidean(matrix, n):
    """Fraction-free Euclidean row reduction for exact (int) input."""
    mat = [row[:] for row in matrix]
    sign = 1

    for col in range(n):
        for row in range(col + 1, n):
            # Bounded loop: number of Euclidean steps for two integers
            # is finite and small (logarithmic in value size), but we
            # still cap it defensively in case of unexpected input.
            guard = 0
            max_iters = 10_000
            while mat[row][col] != 0:
                guard += 1
                if guard > max_iters:
                    raise RuntimeError(
                        "Euclidean reduction did not terminate; "
                        "input may not be exact integers."
                    )

                if mat[col][col] == 0:
                    mat[col], mat[row] = mat[row], mat[col]
                    sign = -sign
                    continue

                q = mat[row][col] // mat[col][col]
                for k in range(col, n):
                    mat[row][k] -= q * mat[col][k]

                if mat[row][col] != 0:
                    mat[col], mat[row] = mat[row], mat[col]
                    sign = -sign

        if mat[col][col] == 0:
            return 0

    det = sign
    for i in range(n):
        det *= mat[i][i]
    return det


def _determinant_float_gaussian(matrix, n, tol=1e-12):
    """
    Standard partial-pivoting Gaussian elimination for float input.

    Division is unavoidable (and appropriate) here: floats are
    inherently approximate, so fraction-free integer tricks don't
    apply. Partial pivoting (choosing the largest available pivot in
    the column) keeps the elimination numerically stable and avoids
    the near-zero-pivot blowups described in the bug report.
    """
    mat = [row[:] for row in matrix]
    sign = 1

    for col in range(n):
        # Partial pivoting: pick the row with the largest absolute
        # value in this column to use as the pivot.
        pivot_row = max(
            range(col, n), key=lambda r: abs(mat[r][col])
        )

        if abs(mat[pivot_row][col]) < tol:
            # Entire column (from here down) is effectively zero.
            return 0.0

        if pivot_row != col:
            mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
            sign = -sign

        pivot = mat[col][col]
        for row in range(col + 1, n):
            if mat[row][col] == 0.0:
                continue
            factor = mat[row][col] / pivot
            for k in range(col, n):
                mat[row][k] -= factor * mat[col][k]
            mat[row][col] = 0.0  # force exact zero, avoid residue drift

    det = float(sign)
    for i in range(n):
        det *= mat[i][i]
    return det