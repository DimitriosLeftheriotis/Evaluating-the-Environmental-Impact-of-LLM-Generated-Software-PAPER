from collections import deque

def dinic(graph, source, sink):
    """
    Compute the maximum flow in a directed graph using Dinic's algorithm.

    Args:
        graph: dict[int, list[tuple[int, int]]]
            Adjacency list mapping each node to a list of (neighbor, capacity).
        source: int
            Source node.
        sink: int
            Sink node.

    Returns:
        int: Maximum flow from source to sink.
    """
    if source == sink:
        return 0

    # Collect all nodes that appear either as keys or neighbors.
    nodes = set(graph.keys())
    for u, edges in graph.items():
        for v, _ in edges:
            nodes.add(v)

    adj = {node: [] for node in nodes}

    class Edge:
        __slots__ = ("to", "rev", "cap")

        def __init__(self, to, rev, cap):
            self.to = to
            self.rev = rev
            self.cap = cap

    def add_edge(u, v, c):
        forward = Edge(v, len(adj[v]), c)
        backward = Edge(u, len(adj[u]), 0)
        adj[u].append(forward)
        adj[v].append(backward)

    for u, edges in graph.items():
        for v, cap in edges:
            add_edge(u, v, cap)

    level = {}

    def bfs():
        level.clear()
        level[source] = 0
        q = deque([source])

        while q:
            u = q.popleft()
            for e in adj[u]:
                if e.cap > 0 and e.to not in level:
                    level[e.to] = level[u] + 1
                    q.append(e.to)

        return sink in level

    def dfs(u, pushed):
        if u == sink:
            return pushed

        while ptr[u] < len(adj[u]):
            e = adj[u][ptr[u]]
            if e.cap > 0 and level.get(e.to, -1) == level[u] + 1:
                flow = dfs(e.to, min(pushed, e.cap))
                if flow:
                    e.cap -= flow
                    adj[e.to][e.rev].cap += flow
                    return flow
            ptr[u] += 1

        return 0

    flow = 0
    INF = float("inf")

    while bfs():
        ptr = {node: 0 for node in nodes}
        while True:
            pushed = dfs(source, INF)
            if pushed == 0:
                break
            flow += pushed

    return flow