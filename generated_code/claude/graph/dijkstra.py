import heapq

def dijkstra(graph, start):
    distances = {start: 0}
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, node = heapq.heappop(heap)

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get(node, []):
            distance = current_dist + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances