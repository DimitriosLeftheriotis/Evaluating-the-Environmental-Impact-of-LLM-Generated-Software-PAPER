def tarjan_scc(graph: dict[int, list[int]]) -> list[list[int]]:
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlink = {}
    sccs = []

    def strongconnect(node: int):
        nonlocal index
        
        # Set the depth index for node to the smallest unused index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        # Consider successors of node
        for neighbor in graph.get(node, []):
            if neighbor not in indices:
                # Successor has not yet been visited; recurse on it
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                # Successor is in stack and hence in the current SCC
                lowlink[node] = min(lowlink[node], indices[neighbor])

        # If node is a root node, pop the stack and generate an SCC
        if lowlink[node] == indices[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    # Call strongconnect for every unvisited node in the graph
    for node in graph:
        if node not in indices:
            strongconnect(node)

    return sccs