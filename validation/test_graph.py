import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_algorithm

LLMS = ["chatgpt", "claude", "gemini"]
ALGORITHMS = ["dijkstra", "bellman_ford", "kruskal", "prim", "tarjan_scc", "dinic"]
PROBLEM_CATEGORY = "graph"

# Small sample graph representations
adj_unweighted = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# Weighted: (neighbor, weight)
adj_weighted = {
    0: [(1, 1.0), (2, 4.0)],
    1: [(0, 1.0), (3, 2.0)],
    2: [(0, 4.0), (3, 1.0)],
    3: [(1, 2.0), (2, 1.0)]
}


def validate_shortest_path(result):
    if isinstance(result, dict):
        assert result[0] == 0, f"Distance to 0 should be 0, got {result[0]}"
        assert result[1] == 1, f"Distance to 1 should be 1, got {result[1]}"
        assert result[3] == 3, f"Distance to 3 should be 3, got {result[3]}"
    elif isinstance(result, list):
        assert result[0] == 0
        assert result[1] == 1
        assert result[3] == 3
    else:
        raise TypeError(f"Unexpected return type: {type(result)}")

def validate_mst(result):
    # Expect list of edges or float MST weight or MST adjacency list.
    # Just check it returns a value and doesn't raise exception.
    assert result is not None, "MST result should not be None"

def validate_scc(result):
    # Returns strongly connected components list
    assert isinstance(result, (list, set)), "SCC should return a list or set of components"

def validate_max_flow(result):
    # Returns flow value (integer or float)
    assert isinstance(result, (int, float)), "Max Flow should return numerical value"

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
                
                if algo in ["dijkstra", "bellman_ford", "prim"]:
                    result = func(adj_weighted, 0)
                    if algo in ["dijkstra", "bellman_ford"]:
                        validate_shortest_path(result)
                    else:
                        validate_mst(result)
                elif algo == "kruskal":
                    result = func(adj_weighted)
                    validate_mst(result)
                elif algo == "tarjan_scc":
                    result = func(adj_unweighted)
                    validate_scc(result)
                elif algo == "dinic":
                    result = func(adj_weighted, 0, 3)
                    validate_max_flow(result)
                
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
