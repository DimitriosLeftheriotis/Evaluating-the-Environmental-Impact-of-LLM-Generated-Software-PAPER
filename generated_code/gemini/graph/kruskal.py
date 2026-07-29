class DisjointSet:
    def __init__(self, vertices):
        # Parent pointer array: each vertex is initially its own parent
        self.parent = {v: v for v in vertices}
        # Rank array to keep the tree flat
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        """Find the root of the set containing `item` with path compression."""
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1, set2):
        """Union two sets by rank. Returns True if merged, False if already in the same set."""
        root1 = self.find(set1)
        root2 = self.find(set2)

        if root1 == root2:
            return False  # Creating a cycle

        # Union by rank heuristic
        if self.rank[root1] < self.rank[root2]:
            root1, root2 = root2, root1
        
        self.parent[root2] = root1
        if self.rank[root1] == self.rank[root2]:
            self.rank[root1] += 1

        return True


def kruskal(graph: dict[int, list[tuple[int, int]]]) -> list[tuple[int, int, int]]:
    # Extract unique undirected edges to avoid duplicate processing
    edges = set()
    for u in graph:
        for v, weight in graph[u]:
            # Store edges in normalized format (min_node, max_node) to deduplicate
            if u < v:
                edges.add((weight, u, v))
            else:
                edges.add((weight, v, u))

    # Sort edges by weight in ascending order
    sorted_edges = sorted(edges, key=lambda edge: edge[0])

    dsu = DisjointSet(graph.keys())
    mst = []

    # Iterate through sorted edges and add them if they don't form a cycle
    for weight, u, v in sorted_edges:
        if dsu.union(u, v):
            mst.append((u, v, weight))

    return mst