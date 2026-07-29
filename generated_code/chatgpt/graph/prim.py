import heapq

def prim(graph, start):
    """
    Compute the Minimum Spanning Tree (MST) of a connected, weighted graph
    using Prim's algorithm.

    Args:
        graph: Dict[int, List[Tuple[int, int]]]
            Adjacency list where graph[u] contains (neighbor, weight).
        start: int
            Starting vertex.

    Returns:
        List[Tuple[int, int, int]]:
            A list of (parent, child, weight) edges in the MST.
    """
    if start not in graph:
        return []

    visited = set()
    mst = []
    min_heap = [(0, None, start)]  # (weight, parent, vertex)

    while min_heap:
        weight, parent, vertex = heapq.heappop(min_heap)

        if vertex in visited:
            continue

        visited.add(vertex)

        if parent is not None:
            mst.append((parent, vertex, weight))

        for neighbor, edge_weight in graph.get(vertex, []):
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, vertex, neighbor))

    return mst