import heapq

def dijkstra(graph: dict[int, list[tuple[int, int]]], start: int) -> dict[int, int]:
    # Initialize distances with infinity, start node distance with 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Priority queue stores tuples of (current_distance, node)
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # If we found a longer path to a node already processed, skip it
        if current_dist > distances[current_node]:
            continue
            
        # Explore neighbors
        for neighbor, weight in graph.get(current_node, []):
            distance = current_dist + weight
            
            # If a shorter path to neighbor is found
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    # Filter out unreachable nodes (optional, based on requirement for reachable nodes)
    return {node: dist for node, dist in distances.items() if dist != float('inf')}