def bellman_ford(graph, source):
    # Initialize distances
    distances = {node: float('inf') for node in graph}
    distances[source] = 0

    # Ensure all nodes referenced as neighbors are also in the distances dict
    for node in graph:
        for neighbor, _ in graph[node]:
            if neighbor not in distances:
                distances[neighbor] = float('inf')

    num_nodes = len(distances)

    # Relax all edges (num_nodes - 1) times
    for _ in range(num_nodes - 1):
        updated = False
        for u in graph:
            if distances[u] == float('inf'):
                continue
            for v, weight in graph[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    updated = True
        if not updated:
            break

    # Check for negative-weight cycles
    for u in graph:
        if distances[u] == float('inf'):
            continue
        for v, weight in graph[u]:
            if distances[u] + weight < distances[v]:
                return None

    return distances