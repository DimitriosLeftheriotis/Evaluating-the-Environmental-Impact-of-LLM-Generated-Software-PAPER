import os
import sys
sys.setrecursionlimit(200000)
import csv
import importlib.util
from codecarbon import EmissionsTracker

LLM = "claude"
PROBLEM = "dynamic_programming"

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
        raise FileNotFoundError(f"Generated code not found at: {module_path}")
    spec = importlib.util.spec_from_file_location(algorithm_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[algorithm_name] = module
    spec.loader.exec_module(module)
    func = getattr(module, algorithm_name, None)
    if func is None:
        raise AttributeError(f"Function `{algorithm_name}` not found in module.")
    return func

# Define algorithm specific parameters
# 1. Fibonacci
fib_mem_scales = [1000, 10000, 100000]

# 2. Knapsack (weights, values, capacity)
knap_scales = [512, 1024, 2048]

# 3. LCS (string1, string2)
lcs_scales = [100, 1000, 5000]

# 4. Matrix Chain (dimensions)
mcm_scales = [10, 50, 100]

# Helper to run a trial
def run_dp_benchmark(algo_name, scale, *args):
    try:
        func = load_algorithm(LLM, PROBLEM, algo_name)
    except Exception as e:
        print(f"[-] Skipping {algo_name}: {e}")
        return

    output_dir = f"results/{LLM}/{PROBLEM}/{algo_name}/"
    os.makedirs(output_dir, exist_ok=True)
    
    with EmissionsTracker(project_name="paper", output_file=f"dp_{scale}.csv", output_dir=output_dir) as tracker:
        result = func(*args)

# Running a single trial (1, 2)
for i in range(1, 2):
    # Fibonacci memoized
    for scale in fib_mem_scales:
        try:
            with open(os.path.join("data", PROBLEM, f"fibonacci_{scale}.csv"), "r") as f:
                reader = csv.reader(f)
                next(reader)
                n = int(next(reader)[0])
            run_dp_benchmark("fibonacci_memoized", scale, n)
        except FileNotFoundError:
            print(f"[-] Data file not found for Fibonacci scale {scale}")

    # Knapsack
    for scale in knap_scales:
        weights = []
        values = []
        try:
            with open(os.path.join("data", PROBLEM, f"knapsack_{scale}.csv"), "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    weights.append(int(row[0]))
                    values.append(int(row[1]))
            capacity = scale * 10
            run_dp_benchmark("knapsack_01", scale, weights, values, capacity)
        except FileNotFoundError:
            print(f"[-] Data file not found for Knapsack scale {scale}")

    # LCS
    for scale in lcs_scales:
        try:
            with open(os.path.join("data", PROBLEM, f"lcs_{scale}.csv"), "r") as f:
                reader = csv.reader(f)
                next(reader)
                row = next(reader)
                s1, s2 = row[0], row[1]
            run_dp_benchmark("lcs", scale, s1, s2)
        except FileNotFoundError:
            print(f"[-] Data file not found for LCS scale {scale}")

    # Matrix Chain
    for scale in mcm_scales:
        dims = []
        try:
            with open(os.path.join("data", PROBLEM, f"matrix_chain_{scale}.csv"), "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    dims.append(int(row[0]))
            run_dp_benchmark("matrix_chain_multiplication", scale, dims)
        except FileNotFoundError:
            print(f"[-] Data file not found for Matrix Chain scale {scale}")

print("[+] Dynamic Programming benchmarking completed.")
