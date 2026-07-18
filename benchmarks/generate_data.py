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
    scales = [100, 1000, 10000]
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
    fib_scales = [30, 35, 40, 10000, 50000, 100000]
    for scale in fib_scales:
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"fibonacci_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["n"])
            writer.writerow([scale])

    knap_scales = [512, 1024, 2048]
    for scale in knap_scales:
        random.seed(scale)
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"knapsack_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["weight", "value"])
            for _ in range(scale):
                w = random.randint(1, 100)
                v = random.randint(10, 1000)
                writer.writerow([w, v])

    lcs_scales = [100, 1000, 5000]
    bases = ["A", "C", "G", "T"]
    for scale in lcs_scales:
        random.seed(scale)
        s1 = "".join(random.choices(bases, k=scale))
        s2 = "".join(random.choices(bases, k=scale))
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"lcs_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["string1", "string2"])
            writer.writerow([s1, s2])

    mcm_scales = [10, 50, 100]
    for scale in mcm_scales:
        random.seed(scale)
        dims = [random.randint(5, 100) for _ in range(scale + 1)]
        filename = os.path.join(DATA_DIR, "dynamic_programming", f"matrix_chain_{scale}.csv")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["dimension"])
            for dim in dims:
                writer.writerow([dim])
    print("[+] Generated DP datasets.")

def generate_matrix_data():
    scales = [64, 128, 256]
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
    create_dirs()
    """
    #generate_sorting_data()
    #generate_graph_data()
    generate_dp_data()
    #generate_matrix_data()
