import heapq

def prim(graph, start):
    """
    Finds the Minimum Spanning Tree (MST) using Prim's algorithm.
    
    :param graph: dict mapping vertex -> list of (neighbor, weight) tuples
    :param start: starting vertex (int)
    :return: list of tuples (parent, child, weight) in the MST
    """
    mst = []
    visited = set([start])
    
    # Priority queue stores tuples of (weight, parent, child)
    # Initialize PQ with all outgoing edges from the start vertex
    min_heap = []
    for neighbor, weight in graph.get(start, []):
        heapq.heappush(min_heap, (weight, start, neighbor))
        
    while min_heap:
        weight, parent, child = heapq.heappop(min_heap)
        
        # If the target node is already visited, skip it
        if child in visited:
            continue
            
        # Add the edge to MST and mark child as visited
        visited.add(child)
        mst.append((parent, child, weight))
        
        # Add all unexplored edges from the newly visited node
        for neighbor, edge_weight in graph.get(child, []):
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, child, neighbor))
                
    return mst