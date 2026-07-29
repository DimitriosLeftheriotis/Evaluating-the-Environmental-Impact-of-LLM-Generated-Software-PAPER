import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_algorithm
sys.setrecursionlimit(200000)
import csv
from codecarbon import EmissionsTracker

LLMs = ["chatgpt", "claude", "gemini"]

PROBLEM = "dynamic_programming"

for llm in LLMs:

    # Define algorithm specific parameters
    # 1. Fibonacci
    fib_mem_scales = [1000, 10000, 100000]

    # 2. Knapsack (weights, values, capacity)
    knap_scales = [10, 100, 1000]

    # 3. LCS (string1, string2)
    lcs_scales = [100, 1000, 10000]

    # 4. Optimal BST (keys, p, q, n)
    bst_scales = [10, 100, 1000]

    # Helper to run a trial
    def run_dp_benchmark(algo_name, scale, *args):
        try:
            func = load_algorithm(llm, PROBLEM, algo_name)
        except Exception as e:
            print(f"[-] Skipping {algo_name}: {e}")
            return

        output_dir = f"results/{llm}/{PROBLEM}/{algo_name}/"
        os.makedirs(output_dir, exist_ok=True)
        
        with EmissionsTracker(project_name="paper", output_file=f"dp_{scale}.csv", output_dir=output_dir) as tracker:
            result = func(*args)

    for i in range(1, 11):
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
            capacity = scale * 10                                                                                                                                                                                                                                               
            try:                                                                                                                                                                                                                                                                
                with open(os.path.join("data", PROBLEM, f"knapsack_{scale}_{capacity}.csv"), "r") as f:                                                                                                                                                                         
                    reader = csv.reader(f)                                                                                                                                                                                                                                      
                    next(reader)                                                                                                                                                                                                                                                
                    for row in reader:                                                                                                                                                                                                                                          
                        weights.append(int(row[0]))                                                                                                                                                                                                                             
                        values.append(int(row[1]))                                                                                                                                                                                                                              
                run_dp_benchmark("knapsack_01", scale, weights, values, capacity)                                                                                                                                                                                               
            except FileNotFoundError:                                                                                                                                                                                                                                           
                print(f"[-] Data file not found for Knapsack scale {scale} and capacity {capacity}")

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

        # Edit Distance
        for scale in lcs_scales:
            try:
                with open(os.path.join("data", PROBLEM, f"edit_distance_{scale}.csv"), "r") as f:
                    reader = csv.reader(f)
                    next(reader)
                    row = next(reader)
                    s1, s2 = row[0], row[1]
                run_dp_benchmark("edit_distance", scale, s1, s2)
            except FileNotFoundError:
                print(f"[-] Data file not found for Edit Distance scale {scale}")

        # Optimal BST
        for scale in bst_scales:
            keys = []
            p = []
            q = []
            try:
                with open(os.path.join("data", PROBLEM, f"optimal_bst_{scale}.csv"), "r") as f:
                    reader = csv.reader(f)
                    next(reader)
                    row0 = next(reader)
                    q.append(float(row0[2]))
                    for row in reader:
                        keys.append(int(row[0]))
                        p.append(float(row[1]))
                        q.append(float(row[2]))
                run_dp_benchmark("optimal_bst", scale, keys, p, q, len(keys))
            except FileNotFoundError:
                print(f"[-] Data file not found for Optimal BST scale {scale}")

print("[+] Dynamic Programming benchmarking completed.")
