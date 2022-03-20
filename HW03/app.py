from collections import defaultdict
from operator import itemgetter
import sys
# import numpy as np


class Node():

    def __init__(self,
                 visited=False,
                 is_branch=False,
                 label='',
                 num_of_visits=1):
        self.visited = visited
        self.is_branch = is_branch
        self.label = label
        self.num_of_visits = num_of_visits
        self.outgoing_edges = []
        self.incoming_edges = []


class Bruijn():

    def __init__(self, k=31):
        self.k = k
        self.graph_data = {}

    def filter_non_repeated_k_mers(self, sequence):
        res = []
        for i in range(0, len(sequence) - self.k + 1):
            res.append(sequence[i:self.k + i])
        return res

    def construct_deBruijn_graph(self, node_instances):
        for index, node in enumerate(node_instances):
            graph = self.graph_data
            curr_node = None
            if node not in graph:
                graph[node] = Node(label=node)
                curr_node = graph[node]
            elif node in graph:
                curr_node = graph[node]
                curr_node.num_of_visits += 1
                self.is_branch = len(curr_node.incoming_edges) > 1 or len(
                    curr_node.outgoing_edges) > 1
            if index - 1 >= 0:
                curr_node.incoming_edges.append(node_instances[index - 1])
            if index + 1 < len(node_instances):
                curr_node.outgoing_edges.append(node_instances[index + 1])

    def filter_graph_by_one_occurence(self):
        for key, data in self.graph_data.items():
            if data.num_of_visits < 2:
                del self.graph_data[key]

    def assemble_trail(self, trail):
        if len(trail) == 0:
            return ""
        result = trail[0][:-1]
        for node in trail:
            result += node[-1]
        return result

    def iterate_helper(self, curr_node: Node, result: str) -> str:
        # validate curr_node if it's visited or is a branching node
        if curr_node.visited or curr_node.is_branch:
            return result

        incoming_edges = curr_node.incoming_edges
        outgoing_edges = curr_node.outgoing_edges

        # mark current node as visited
        curr_node.visited = True

        # recursively iterate through all incoming + outgoing node
        incoming_path, outgoing_path = '', ''
        for edge in incoming_edges:
            incoming_node = self.graph_data[edge]
            incoming_path = self.iterate_helper(incoming_node, result)
            # print(edge)
            # print('incoming_path', incoming_path)
        for edge in outgoing_edges:
            outgoing_node = self.graph_data[edge]
            outgoing_path = self.iterate_helper(outgoing_node, result)
            # print('outgoing_path', outgoing_path)
        # print('return values', incoming_path + curr_node.label + outgoing_path)
        return incoming_path + curr_node.label + outgoing_path

    def iterate_graph(self):
        substrings = self.graph_data.keys()
        path = ''
        for substring in substrings:
            print(substring)
            substringGraphNode = self.graph_data[substring]
            print(substringGraphNode.incoming_edges)
            path = self.iterate_helper(substringGraphNode, '')
        print(path)


def parse_string_inputs():
    '''
    A method to parse input data
    '''
    curr_input = []
    for line in sys.stdin:
        row = line.replace("\n", "")
        curr_input.append(row)

    return curr_input


def main(argv):

    if len(argv) > 1:
        k_mers = itemgetter(1)(argv)
        bruijn_graph = Bruijn(k=int(k_mers))
    else:
        bruijn_graph = Bruijn(k=5)

    sequence_inputs = parse_string_inputs()

    labeled_nodes = []

    for sequence in sequence_inputs:
        labeled_nodes += bruijn_graph.filter_non_repeated_k_mers(sequence)
        bruijn_graph.construct_deBruijn_graph(labeled_nodes)
    # print(bruijn_graph.graph_data["Once_"].incoming_edges)
    bruijn_graph.iterate_graph()

    # bruijn_graph.count_repeated_nodes(labeled_nodes, total_nodes)
    # m = bruijn_graph.make_node_edge_map(graph_nodes[1])
    # graph_nodes = list(graph_nodes)
    # start = graph_nodes[2][0] if (len(graph_nodes[2]) > 0) else graph_nodes[0][0]
    # t = bruijn_graph.eulerian_trail(m,start)
    # print(t)
    # a = bruijn_graph.assemble_trail(t)
    # print(a)

    # bruijn_graph.filter_graph_by_one_occurence()


if __name__ == '__main__':
    main(sys.argv)
