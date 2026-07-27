import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_algorithm

LLMS = ["chatgpt", "claude", "gemini"]
ALGORITHMS = ["bubble_sort", "merge_sort", "heap_sort", "radix_sort", "counting_sort"]
PROBLEM_CATEGORY = "sorting"

# Small sample input to check correctness
# Note: For counting/radix sort, non-negative integers are expected.
TEST_ARRAY = [42, 7, 91, 15, 63, 28, 84, 3, 56, 19]
EXPECTED_OUTPUT = sorted(TEST_ARRAY)


def main():
    print(f"=== Starting Validation for {PROBLEM_CATEGORY.upper()} ===")
    
    passed_count = 0
    failed_count = 0
    missing_count = 0

    for llm in LLMS:
        print(f"\nEvaluating LLM: {llm}")
        for algo in ALGORITHMS:
            try:
                # Load the function dynamically
                func = load_algorithm(llm, PROBLEM_CATEGORY, algo)
                
                # Execute the function on the test data
                result = func(TEST_ARRAY.copy())
                
                # Check correctness
                assert result == EXPECTED_OUTPUT, f"Expected {EXPECTED_OUTPUT}, but got {result}"
                
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