import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_algorithm

LLMS = ["chatgpt", "claude", "gemini"]
ALGORITHMS = ["naive_matrix_multiplication", "strassen_algorithm", "matrix_transpose", "lu_decomposition", "matrix_determinant"]
PROBLEM_CATEGORY = "matrix"

# Test matrices
mat_A = [
    [1.0, 2.0],
    [3.0, 4.0]
]
mat_B = [
    [2.0, 0.0],
    [1.0, 2.0]
]

# Expected results
expected_mul = [
    [4.0, 4.0],
    [10.0, 8.0]
]
expected_transpose = [
    [1.0, 3.0],
    [2.0, 4.0]
]
expected_det = -2.0


def main():
    print(f"=== Starting Validation for {PROBLEM_CATEGORY.upper()} ===")
    
    passed_count = 0
    failed_count = 0
    missing_count = 0

    for llm in LLMS:
        print(f"\nEvaluating LLM: {llm}")
        for algo in ALGORITHMS:
            try:
                func = load_algorithm(llm, PROBLEM_CATEGORY, algo)
                
                if algo in ["naive_matrix_multiplication", "strassen_algorithm"]:
                    result = func(mat_A, mat_B)
                    rounded_result = [[round(x, 2) for x in row] for row in result]
                    assert rounded_result == expected_mul, f"Expected {expected_mul}, got {rounded_result}"
                
                elif algo == "matrix_transpose":
                    result = func(mat_A)
                    rounded_result = [[round(x, 2) for x in row] for row in result]
                    assert rounded_result == expected_transpose, f"Expected {expected_transpose}, got {rounded_result}"
                
                elif algo == "matrix_determinant":
                    result = func(mat_A)
                    assert round(result, 2) == expected_det, f"Expected {expected_det}, got {result}"
                
                elif algo == "lu_decomposition":
                    L, U = func(mat_A)
                    assert len(L) == 2 and len(U) == 2, "LU dimensions should be 2x2"
                
                print(f"  [PASS] {algo}")
                passed_count += 1
            except FileNotFoundError:
                print(f"  [MISSING] {algo}: File not generated yet")
                missing_count += 1
            except Exception as e:
                print(f"  [FAIL] {algo}: Error: {e}")
                failed_count += 1
                
    print(f"\nValidation Summary: {passed_count} passed, {failed_count} failed, {missing_count} missing.")

if __name__ == "__main__":
    main()
