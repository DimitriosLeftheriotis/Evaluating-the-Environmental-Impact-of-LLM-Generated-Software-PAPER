def kruskal(graph):
    # Build a unique set of edges from adjacency list
    edges = []
    seen = set()
    for u in graph:
        for v, weight in graph[u]:
            key = (min(u, v), max(u, v), weight)
            if key not in seen:
                seen.add(key)
                edges.append((weight, u, v))

    # Sort edges by weight
    edges.sort(key=lambda e: e[0])

    # Union-Find (Disjoint Set Union) structures
    parent = {}
    rank = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        if rank[root_x] < rank[root_y]:
            root_x, root_y = root_y, root_x
        parent[root_y] = root_x
        if rank[root_x] == rank[root_y]:
            rank[root_x] += 1
        return True

    for node in graph:
        parent[node] = node
        rank[node] = 0

    mst = []
    for weight, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))

    return mst