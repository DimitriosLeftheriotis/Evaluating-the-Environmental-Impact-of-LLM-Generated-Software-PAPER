def kruskal(graph):
    parent = {}
    rank = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx = find(x)
        ry = find(y)

        if rx == ry:
            return False

        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1

        return True

    vertices = set(graph.keys())
    for u in graph:
        for v, _ in graph[u]:
            vertices.add(v)

    for v in vertices:
        parent[v] = v
        rank[v] = 0

    edges = []
    seen = set()

    for u in graph:
        for v, weight in graph[u]:
            edge = (min(u, v), max(u, v))
            if edge not in seen:
                seen.add(edge)
                edges.append((weight, u, v))

    edges.sort()

    mst = []
    for weight, u, v in edges:
        if union(u, v):
            mst.append((u, v, weight))

    return mst