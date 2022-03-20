def visualize_debruijn(self, G):
    nodes = G[0]
    edges = G[1]
    dot_str = 'digraph "DeBruijn graph" {\n '
    for node in nodes:
        dot_str += '    %s [label="%s"] ;\n' % (node, node)
    for src, dst in edges:
        dot_str += '    %s->%s;\n' % (src, dst)
    return dot_str + '}\n'
