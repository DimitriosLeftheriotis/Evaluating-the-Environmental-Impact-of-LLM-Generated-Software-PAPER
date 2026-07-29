def bellman_ford(graph, source):
    # Collect all nodes, including nodes that only appear as neighbors
    nodes = set(graph.keys())
    for edges in graph.values():
        for neighbor, _ in edges:
            nodes.add(neighbor)

    # Initialize distances
    distances = {node: float('inf') for node in nodes}
    distances[source] = 0

    # Relax all edges |V| - 1 times
    for _ in range(len(nodes) - 1):
        updated = False

        for node, edges in graph.items():
            if distances[node] == float('inf'):
                continue

            for neighbor, weight in edges:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    updated = True

        # Early exit if no updates occurred
        if not updated:
            break

    # Check for negative-weight cycles
    for node, edges in graph.items():
        if distances[node] == float('inf'):
            continue

        for neighbor, weight in edges:
            if distances[node] + weight < distances[neighbor]:
                return None

    return distances