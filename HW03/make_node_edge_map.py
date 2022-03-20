def make_node_edge_map(self, edges):
    # print("Edges: ", edges)
    node_edge_map = {}
    for edge in edges:
        node = edge[0]
        if node in node_edge_map:
            node_edge_map[node].append(edge[1])
        else:
            node_edge_map[node] = [edge[1]]
    return node_edge_map
