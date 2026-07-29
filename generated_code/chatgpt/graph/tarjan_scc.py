def tarjan_scc(graph):
    """
    Compute the strongly connected components (SCCs) of a directed graph
    using Tarjan's algorithm.

    Args:
        graph (dict[int, list[int]]): Adjacency list representation of the graph.

    Returns:
        list[list[int]]: A list of strongly connected components, where each
        component is represented as a list of vertices.
    """
    index = 0
    indices = {}
    lowlink = {}
    stack = []
    on_stack = set()
    sccs = []

    # Include vertices that only appear as neighbors.
    vertices = set(graph.keys())
    for neighbors in graph.values():
        vertices.update(neighbors)

    def strongconnect(v):
        nonlocal index

        indices[v] = index
        lowlink[v] = index
        index += 1

        stack.append(v)
        on_stack.add(v)

        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            sccs.append(component)

    for v in vertices:
        if v not in indices:
            strongconnect(v)

    return sccs