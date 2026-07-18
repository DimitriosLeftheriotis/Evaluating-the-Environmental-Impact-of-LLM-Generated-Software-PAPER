import os
import sys
import csv
import importlib.util
from codecarbon import EmissionsTracker

LLMs = ["chatgpt", "claude", "gemini"]

PROBLEM = "graph"

for llm in LLMs:
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

    scales = [100, 1000, 10000]
    algorithms = ["bfs", "dfs", "dijkstra", "bellman_ford", "floyd_warshall"]

    for scale in scales:
        # 1. Load the graph edge list CSV
        edges = []
        csv_path = os.path.join("data", PROBLEM, f"graph_{scale}.csv")
        
        try:
            with open(csv_path, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    u, v, w = int(row[0]), int(row[1]), float(row[2])
                    edges.append((u, v, w))
        except FileNotFoundError:
            print(f"[-] Data file not found: {csv_path}. Please run generate_data.py first.")
            continue

        # 2. Build the pure-Python adjacency list representations
        adj_unweighted = {}
        adj_weighted = {}

        # Initialize empty lists for all nodes (0 to scale-1)
        for node in range(scale):
            adj_unweighted[node] = []
            adj_weighted[node] = []

        for u, v, w in edges:
            adj_unweighted[u].append(v)
            adj_unweighted[v].append(u)
            adj_weighted[u].append((v, w))
            adj_weighted[v].append((u, w))

        # 3. Execute Benchmarks (1 trial)
        for i in range(1, 2):
            for algo in algorithms:
                try:
                    func = load_algorithm(llm, PROBLEM, algo)
                except Exception as e:
                    print(f"[-] Skipping {algo}: {e}")
                    continue

                output_dir = f"results/{llm}/{PROBLEM}/{algo}/"
                os.makedirs(output_dir, exist_ok=True)
                
                with EmissionsTracker(project_name="paper", output_file=f"graph_{scale}.csv", output_dir=output_dir) as tracker:
                    if algo in ["bfs", "dfs"]:
                        result = func(adj_unweighted, 0)
                    elif algo in ["dijkstra", "bellman_ford"]:
                        result = func(adj_weighted, 0)
                    elif algo == "floyd_warshall":
                        result = func(adj_weighted)

print("[+] Graph benchmarking completed.")
