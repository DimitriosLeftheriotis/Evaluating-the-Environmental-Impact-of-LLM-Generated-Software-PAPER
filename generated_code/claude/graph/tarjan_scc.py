def tarjan_scc(graph):
    """
    Tarjan's algorithm for finding strongly connected components (SCCs)
    in a directed graph.

    Args:
        graph: dict mapping int -> list of int, representing adjacency list.
               Nodes referenced only as neighbors (not as keys) are handled
               as having no outgoing edges.

    Returns:
        List of lists, each sublist containing the vertices of one SCC.
    """
    index_counter = [0]
    index = {}
    lowlink = {}
    on_stack = {}
    stack = []
    result = []

    # Collect all nodes (including those only appearing as neighbors)
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for node in all_nodes:
        index[node] = -1
        lowlink[node] = -1
        on_stack[node] = False

    def strongconnect(start_node):
        # Iterative implementation using an explicit work stack
        # Each frame: (node, iterator_index_into_neighbors)
        work_stack = [(start_node, 0)]

        while work_stack:
            node, child_idx = work_stack[-1]

            if child_idx == 0:
                # First time visiting this node
                index[node] = index_counter[0]
                lowlink[node] = index_counter[0]
                index_counter[0] += 1
                stack.append(node)
                on_stack[node] = True

            neighbors = graph.get(node, [])
            recursed = False

            i = child_idx
            while i < len(neighbors):
                successor = neighbors[i]
                if index[successor] == -1:
                    # Successor not visited, recurse into it
                    work_stack[-1] = (node, i + 1)
                    work_stack.append((successor, 0))
                    recursed = True
                    break
                elif on_stack[successor]:
                    lowlink[node] = min(lowlink[node], index[successor])
                i += 1

            if recursed:
                continue

            # Finished processing all neighbors of node
            work_stack.pop()

            if work_stack:
                parent = work_stack[-1][0]
                lowlink[parent] = min(lowlink[parent], lowlink[node])

            # If node is a root node, pop the stack and form an SCC
            if lowlink[node] == index[node]:
                component = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    component.append(w)
                    if w == node:
                        break
                result.append(component)

    for node in all_nodes:
        if index[node] == -1:
            strongconnect(node)

    return result