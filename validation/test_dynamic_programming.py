import os
import sys
import importlib.util

sys.setrecursionlimit(200000)

LLMS = ["chatgpt", "claude", "gemini"]
PROBLEM_CATEGORY = "dynamic_programming"

def load_algorithm(llm, problem_category, algorithm_name):
    module_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 
        "..", 
        "generated_code", 
        llm, 
        problem_category, 
        f"{algorithm_name}.py"
    ))
    
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Missing file: {module_path}")
        
    spec = importlib.util.spec_from_file_location(algorithm_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[algorithm_name] = module
    spec.loader.exec_module(module)
    
    func = getattr(module, algorithm_name, None)
    if func is None:
        raise AttributeError(f"Function `{algorithm_name}` not found in module.")
    return func

def main():
    print(f"=== Starting Validation for {PROBLEM_CATEGORY.upper()} ===")
    
    passed_count = 0
    failed_count = 0
    missing_count = 0

    # Test cases
    # 1. Fibonacci
    fib_n = 10
    
    # 2. Knapsack
    weights = [1, 2, 3]
    values = [10, 15, 40]
    capacity = 5
    expected_knapsack = 55

    # 3. LCS
    s1 = "abcde"
    s2 = "ace"

    # 4. Edit Distance (Levenshtein)
    edit_s1 = "kitten"
    edit_s2 = "sitting"
    expected_edit = 3

    # 5. Optimal BST
    keys = [10, 12, 20]
    p = [0.34, 0.08, 0.15]
    q = [0.05, 0.10, 0.10, 0.18]
    n = len(keys)

    for llm in LLMS:
        print(f"\nEvaluating LLM: {llm}")
        
        # Fibonacci Memoized
        try:
            func = load_algorithm(llm, PROBLEM_CATEGORY, "fibonacci_memoized")
            result = func(fib_n)
            assert result in [55, 89], f"Expected 55 or 89, got {result}"
            print("  [PASS] fibonacci_memoized")
            passed_count += 1
        except FileNotFoundError:
            print("  [MISSING] fibonacci_memoized: File not generated yet")
            missing_count += 1
        except Exception as e:
            print(f"  [FAIL] fibonacci_memoized: Error: {e}")
            failed_count += 1

        # Knapsack 01
        try:
            func = load_algorithm(llm, PROBLEM_CATEGORY, "knapsack_01")
            result = func(weights, values, capacity)
            assert result == expected_knapsack, f"Expected {expected_knapsack}, got {result}"
            print("  [PASS] knapsack_01")
            passed_count += 1
        except FileNotFoundError:
            print("  [MISSING] knapsack_01: File not generated yet")
            missing_count += 1
        except Exception as e:
            print(f"  [FAIL] knapsack_01: Error: {e}")
            failed_count += 1

        # LCS
        try:
            func = load_algorithm(llm, PROBLEM_CATEGORY, "lcs")
            result = func(s1, s2)
            if isinstance(result, str):
                assert len(result) == 3, f"Expected length 3, got '{result}'"
            else:
                assert result == 3, f"Expected length 3, got {result}"
            print("  [PASS] lcs")
            passed_count += 1
        except FileNotFoundError:
            print("  [MISSING] lcs: File not generated yet")
            missing_count += 1
        except Exception as e:
            print(f"  [FAIL] lcs: Error: {e}")
            failed_count += 1

        # Edit Distance
        try:
            func = load_algorithm(llm, PROBLEM_CATEGORY, "edit_distance")
            result = func(edit_s1, edit_s2)
            assert result == expected_edit, f"Expected {expected_edit}, got {result}"
            print("  [PASS] edit_distance")
            passed_count += 1
        except FileNotFoundError:
            print("  [MISSING] edit_distance: File not generated yet")
            missing_count += 1
        except Exception as e:
            print(f"  [FAIL] edit_distance: Error: {e}")
            failed_count += 1

        # Optimal BST
        try:
            func = load_algorithm(llm, PROBLEM_CATEGORY, "optimal_bst")
            result = func(keys, p, q, n)
            assert isinstance(result, (int, float)), f"Expected float/int cost, got {type(result)}"
            print("  [PASS] optimal_bst")
            passed_count += 1
        except FileNotFoundError:
            print("  [MISSING] optimal_bst: File not generated yet")
            missing_count += 1
        except Exception as e:
            print(f"  [FAIL] optimal_bst: Error: {e}")
            failed_count += 1

    print(f"\nValidation Summary: {passed_count} passed, {failed_count} failed, {missing_count} missing.")

if __name__ == "__main__":
    main()
