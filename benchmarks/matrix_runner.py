import os
import sys
import csv
import importlib.util
from codecarbon import EmissionsTracker

LLMs = ["chatgpt", "claude", "gemini"]
PROBLEM = "matrix"

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

    scales = [10, 100, 1000]
    algorithms = ["naive_matrix_multiplication", "strassen_algorithm", "matrix_transpose", "lu_decomposition", "matrix_determinant"]

    def load_matrix(filepath):
        matrix = []
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                matrix.append([float(x) for x in row])
        return matrix

    for scale in scales:
        # Load matrices A and B
        try:
            mat_A = load_matrix(os.path.join("data", PROBLEM, f"matrix_{scale}_A.csv"))
            mat_B = load_matrix(os.path.join("data", PROBLEM, f"matrix_{scale}_B.csv"))
        except FileNotFoundError:
            print(f"[-] Data file not found for Matrix scale {scale}. Please run generate_data.py first.")
            continue

        # Running a single trial (1, 2)
        for i in range(1, 2):
            for algo in algorithms:
                try:
                    func = load_algorithm(llm, PROBLEM, algo)
                except Exception as e:
                    print(f"[-] Skipping {algo}: {e}")
                    continue

                output_dir = f"results/{llm}/{PROBLEM}/{algo}/"
                os.makedirs(output_dir, exist_ok=True)
                
                with EmissionsTracker(project_name="paper", output_file=f"matrix_{scale}.csv", output_dir=output_dir) as tracker:
                    if algo in ["naive_matrix_multiplication", "strassen_algorithm"]:
                        result = func(mat_A, mat_B)
                    elif algo in ["matrix_transpose", "lu_decomposition", "matrix_determinant"]:
                        result = func(mat_A)

print("[+] Matrix benchmarking completed.")
