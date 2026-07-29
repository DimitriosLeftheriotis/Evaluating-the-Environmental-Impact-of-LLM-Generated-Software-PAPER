import heapq

def prim(graph, start):
    """
    Compute the Minimum Spanning Tree (MST) of a graph using Prim's algorithm.

    Parameters:
        graph (dict[int, list[tuple[int, int]]]): Adjacency list representation
            of the graph, mapping each vertex to a list of (neighbor, weight) tuples.
        start (int): The vertex to start building the MST from.

    Returns:
        list[tuple[int, int, int]]: List of (parent, child, weight) edges forming the MST.
    """
    mst_edges = []
    visited = set([start])
    # heap entries: (weight, parent, child)
    heap = []

    for neighbor, weight in graph.get(start, []):
        heapq.heappush(heap, (weight, start, neighbor))

    while heap and len(visited) < len(graph):
        weight, parent, child = heapq.heappop(heap)

        if child in visited:
            continue

        visited.add(child)
        mst_edges.append((parent, child, weight))

        for neighbor, w in graph.get(child, []):
            if neighbor not in visited:
                heapq.heappush(heap, (w, child, neighbor))

    return mst_edges