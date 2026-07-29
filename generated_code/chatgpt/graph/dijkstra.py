import heapq

def dijkstra(graph, start):
    """
    Compute the shortest distances from the starting node to all reachable nodes
    in a weighted graph using Dijkstra's algorithm.

    Args:
        graph (dict[int, list[tuple[int, float]]]):
            Adjacency list mapping each node to a list of (neighbor, weight) pairs.
        start (int): The starting node.

    Returns:
        dict[int, float]: A mapping from each reachable node to its shortest
        distance from the starting node.
    """
    distances = {start: 0}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, node = heapq.heappop(priority_queue)

        # Skip outdated queue entries.
        if current_distance > distances[node]:
            continue

        for neighbor, weight in graph.get(node, []):
            new_distance = current_distance + weight

            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances