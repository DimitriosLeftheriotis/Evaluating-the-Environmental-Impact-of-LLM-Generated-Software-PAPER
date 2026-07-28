import os
import csv
import random
import networkx as nx

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def create_dirs():
    for sub in ["sorting", "graph", "dynamic_programming", "matrix"]:
        os.makedirs(os.path.join(DATA_DIR, sub), exist_ok=True)

def generate_sorting_data():
    scales = [1000, 10000, 100000]
    for scale in scales:
        random.seed(scale)
        numbers = random.sample(range(10**6 + 1), scale)
        filename = os.path.join(DATA_DIR, "sorting", f"unordered_numbers_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["number"])
            for num in numbers:
                writer.writerow([num])
    print("[+] Generated Sorting datasets.")

def generate_graph_data():
    scales = [10, 100, 1000]
    density = 0.75
    for scale in scales:
        G = nx.erdos_renyi_graph(n=scale, p=density, seed=scale, directed=False)
        random.seed(scale)
        
        filename = os.path.join(DATA_DIR, "graph", f"graph_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["source", "target", "weight"])
            for u, v in G.edges():
                weight = round(random.uniform(1.0, 50.0), 2)
                writer.writerow([u, v, weight])
    print("[+] Generated Graph datasets.")

def generate_dp_data():
    fib_scales = [1000, 10000, 100000]
    for scale in fib_scales:
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"fibonacci_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["n"])
            writer.writerow([scale])

    knap_scales = [10, 100, 1000]
    capacities = [100, 1000, 10000]

    knap_dir = os.path.join(DATA_DIR, "dynamic_programming")

    for scale in knap_scales:
        for capacity in capacities:
            random.seed(scale * 100000 + capacity)

            target_total_weight = 2 * capacity

            # Generate random weights
            weights = [random.randint(1, 100) for _ in range(scale)]

            # Scale them so the total weight is about 2 * capacity
            current_total = sum(weights)
            factor = target_total_weight / current_total
            weights = [max(1, round(w * factor)) for w in weights]

            # Fix rounding errors so sum(weights) == 2 * capacity
            diff = target_total_weight - sum(weights)

            weights[-1] += diff

            if weights[-1] < 1:
                deficit = 1 - weights[-1]
                weights[-1] = 1

                for i in range(scale - 1):
                    take = min(deficit, weights[i] - 1)
                    weights[i] -= take
                    deficit -= take
                    if deficit == 0:
                        break

            filename = os.path.join(
                knap_dir,
                f"knapsack_{scale}_{capacity}.csv"
            )

            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["capacity", capacity])
                writer.writerow(["weight", "value"])

                for weight in weights:
                    value = random.randint(10, 1000)
                    writer.writerow([weight, value])

    # it will be the same for Edit Distance
    lcs_scales = [100, 1000, 10000]
    bases = ["A", "C", "G", "T"]
    for scale in lcs_scales:
        random.seed(scale)
        s1 = "".join(random.choices(bases, k=scale))
        s2 = "".join(random.choices(bases, k=scale))
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"lcs_{scale}.csv")
        filename2 = os.path.join(DATA_DIR, "dynamic_programming", f"edit_distance_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["string1", "string2"])
            writer.writerow([s1, s2])
        with open(filename2, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["string1", "string2"])
            writer.writerow([s1, s2])

    bst_scales = [10, 100, 1000]
    for scale in bst_scales:
        random.seed(scale)
        keys = sorted(random.sample(range(1, scale * 10), scale))
        freqs = [round(random.uniform(0.1, 10.0), 4) for _ in range(2 * scale + 1)]
        total = sum(freqs)
        freqs = [round(f / total, 6) for f in freqs]
        p = freqs[:scale]
        q = freqs[scale:]
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"optimal_bst_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["key", "p", "q"])
            writer.writerow(["", "", q[0]])
            for idx in range(scale):
                writer.writerow([keys[idx], p[idx], q[idx + 1]])
    print("[+] Generated DP datasets.")

def generate_matrix_data():
    scales = [10, 100, 1000]
    for scale in scales:
        random.seed(scale)
        for mat_label in ["A", "B"]:
            filename = os.path.join(DATA_DIR, "matrix", f"matrix_{scale}_{mat_label}.csv")
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                for _ in range(scale):
                    row = [round(random.uniform(-10.0, 10.0), 4) for _ in range(scale)]
                    writer.writerow(row)
    print("[+] Generated Matrix datasets.")

if __name__ == "__main__":
    """
    # runs just the first time
    create_dirs()
    """
    generate_sorting_data()
    generate_graph_data()
    generate_dp_data()
    generate_matrix_data()
    print("it works")
    