def bellman_ford(edges, n, source):
    """
    Compute shortest path distances from a source vertex using the Bellman-Ford algorithm.

    Args:
        edges: List of tuples (u, v, weight) representing directed edges.
        n: Number of vertices, assumed to be labeled 0 through n-1.
        source: Source vertex.

    Returns:
        A dictionary mapping each vertex to its shortest distance from the source.
        If a negative-weight cycle is reachable from the source, returns None.
    """
    distances = {v: float("inf") for v in range(n)}
    distances[source] = 0

    # Relax edges up to n - 1 times
    for _ in range(n - 1):
        updated = False
        for u, v, weight in edges:
            if distances[u] != float("inf") and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                updated = True
        if not updated:
            break

    # Check for negative-weight cycles reachable from the source
    for u, v, weight in edges:
        if distances[u] != float("inf") and distances[u] + weight < distances[v]:
            return None

    return distances