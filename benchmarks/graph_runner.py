import os
import sys
sys.setrecursionlimit(10000)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_algorithm
import csv
from codecarbon import EmissionsTracker

LLMs = ["chatgpt", "claude", "gemini"]

PROBLEM = "graph"

for llm in LLMs:

    scales = [10, 100, 1000]
    algorithms = ["dijkstra", "bellman_ford", "kruskal", "prim", "tarjan_scc", "dinic"]

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
        for algo in algorithms:
            try:
                func = load_algorithm(llm, PROBLEM, algo)
            except Exception as e:
                print(f"[-] Skipping {algo}: {e}")
                continue

            output_dir = f"results/{llm}/{PROBLEM}/{algo}/"
            os.makedirs(output_dir, exist_ok=True)
            
            for i in range(1, 11):
                with EmissionsTracker(project_name="paper", output_file=f"{algo}_{scale}.csv", output_dir=output_dir) as tracker:
                    if algo in ["dijkstra", "bellman_ford", "prim"]:
                        result = func(adj_weighted, 0)
                    elif algo == "kruskal":
                        result = func(adj_weighted)
                    elif algo == "tarjan_scc":
                        result = func(adj_unweighted)
                    elif algo == "dinic":
                        result = func(adj_weighted, 0, scale - 1)

print("[+] Graph benchmarking completed.")
