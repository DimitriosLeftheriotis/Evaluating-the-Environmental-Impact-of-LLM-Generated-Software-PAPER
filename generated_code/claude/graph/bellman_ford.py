def bellman_ford(edges, n, source):
    INF = float('inf')
    dist = {i: INF for i in range(n)}
    dist[source] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, weight in edges:
            if dist[u] != INF and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                updated = True
        if not updated:
            break

    for u, v, weight in edges:
        if dist[u] != INF and dist[u] + weight < dist[v]:
            return None

    return dist