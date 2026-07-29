def bellman_ford(edges, n, source):
    # Initialize distances from source to all other vertices as infinity
    distances = {i: float('inf') for i in range(n)}
    distances[source] = 0

    # Relax all edges n - 1 times
    for _ in range(n - 1):
        updated = False
        for u, v, weight in edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                updated = True
        # Optimization: If no distances were updated, we can stop early
        if not updated:
            break

    # Check for negative-weight cycles
    for u, v, weight in edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            return None

    return distances