from collections import deque, defaultdict


def dinic(graph, source, sink):
    """
    Compute the maximum flow from `source` to `sink` using Dinic's algorithm.

    Parameters:
        graph: dict[int, list[tuple[int, int]]]
            Adjacency list mapping a node to a list of (neighbor, capacity) tuples.
        source: int
            The source node.
        sink: int
            The sink node.

    Returns:
        int: The maximum flow value from source to sink.
    """

    # Build a unified list of all nodes referenced anywhere in the graph
    nodes = set(graph.keys())
    for u, edges in graph.items():
        for v, cap in edges:
            nodes.add(v)
    nodes.add(source)
    nodes.add(sink)

    # Adjacency representation for the residual graph:
    # adj[u] = list of edge indices (into the `edges` array) that start at u
    adj = defaultdict(list)
    # Each edge is represented as [to, capacity, index_of_reverse_edge]
    edges = []

    def add_edge(u, v, cap):
        # Forward edge
        adj[u].append(len(edges))
        edges.append([v, cap, len(edges) + 1])
        # Reverse edge (initial capacity 0)
        adj[v].append(len(edges))
        edges.append([u, 0, len(edges) - 1])

    for u, edge_list in graph.items():
        for v, cap in edge_list:
            add_edge(u, v, cap)

    def bfs():
        level = {n: -1 for n in nodes}
        level[source] = 0
        q = deque([source])
        while q:
            u = q.popleft()
            for eid in adj[u]:
                to, cap, _ = edges[eid]
                if cap > 0 and level[to] < 0:
                    level[to] = level[u] + 1
                    q.append(to)
        return level if level[sink] >= 0 else None

    def dfs(u, pushed, level, it):
        if u == sink or pushed == 0:
            return pushed
        while it[u] < len(adj[u]):
            eid = adj[u][it[u]]
            to, cap, rev = edges[eid]
            if cap > 0 and level[to] == level[u] + 1:
                d = dfs(to, min(pushed, cap), level, it)
                if d > 0:
                    edges[eid][1] -= d
                    edges[rev][1] += d
                    return d
            it[u] += 1
        return 0

    max_flow = 0
    while True:
        level = bfs()
        if level is None:
            break
        it = {n: 0 for n in nodes}
        while True:
            pushed = dfs(source, float('inf'), level, it)
            if pushed == 0:
                break
            max_flow += pushed

    return int(max_flow)