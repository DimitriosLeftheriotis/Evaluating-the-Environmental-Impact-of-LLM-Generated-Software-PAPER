def bellman_ford(graph: dict, source: int):
    # Initialize distances for all nodes in the graph to infinity
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    num_vertices = len(graph)

    # Relax edges up to |V| - 1 times
    for _ in range(num_vertices - 1):
        updated = False
        for node in graph:
            if distances[node] == float('inf'):
                continue
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    updated = True
        
        # Optimization: stop early if no distances changed in this iteration
        if not updated:
            break

    # Check for negative-weight cycles
    for node in graph:
        if distances[node] == float('inf'):
            continue
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                return None

    return distances